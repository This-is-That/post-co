import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import torchvision.models as models
import os
import csv
import torch.nn.functional as F
from tqdm.auto import tqdm
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
from torch.utils.data import DataLoader
from model import SimSiam
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts

def cutmix_data(x, alpha=1.0):
    """Apply CutMix augmentation to a batch of images."""
    lam = np.random.beta(alpha, alpha)
    batch_size = x.size(0)
    index = torch.randperm(batch_size).to(x.device)

    bbx1, bby1, bbx2, bby2 = rand_bbox(x.size(), lam)
    x[:, :, bbx1:bbx2, bby1:bby2] = x[index, :, bbx1:bbx2, bby1:bby2]
    lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (x.size(-1) * x.size(-2)))
    return x, index, lam

def rand_bbox(size, lam):
    """Generate a random bounding box."""
    W = size[2]
    H = size[3]
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(W * cut_rat)
    cut_h = int(H * cut_rat)

    cx = np.random.randint(W)
    cy = np.random.randint(H)

    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bby2 = np.clip(cy + cut_h // 2, 0, H)

    return bbx1, bby1, bbx2, bby2

def D(p, z):
    """Negative cosine similarity between p and z"""
    z = z.detach()  # Stop gradient
    p = F.normalize(p, dim=1)  # Normalize p
    z = F.normalize(z, dim=1)  # Normalize z
    return 1 - (p * z).sum(dim=1).mean()

def simsiam_cutmix_loss_fn(p1, z1, p2, z2, index, lam):
    """SimSiam loss function with CutMix integration"""
    return lam * D(p1, z2) + (1 - lam) * D(p1, z2[index]) + lam * D(p2, z1) + (1 - lam) * D(p2, z1[index])
# Custom Dataset
class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = [os.path.join(root_dir, fname) for fname in os.listdir(root_dir) if fname.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image

# 데이터 로더 함수
def get_custom_data_loader(root_dir, batch_size, transform, shuffle=True, num_workers=4):
    dataset = CustomDataset(root_dir=root_dir, transform=transform)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
    return data_loader

class EarlyStopping:
    def __init__(self, patience=5, min_delta=0, save_path='./best_model.pth'):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
        self.save_path = save_path

    def __call__(self, val_loss, model):
        if self.best_loss is None:
            self.best_loss = val_loss
            self.save_checkpoint(model)
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0
            self.save_checkpoint(model)

    def save_checkpoint(self, model):
        """Save the current best model."""
        torch.save(model.state_dict(), self.save_path)
        print(f"Model saved with loss {self.best_loss}")

# 모델 및 최적화 설정
def setup_model_and_optimizer(base_encoder, dim, pred_dim, lr, T_0, T_mult, eta_min):
    model = SimSiam(base_encoder=base_encoder, dim=dim, pred_dim=pred_dim)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=T_0, T_mult=T_mult, eta_min=eta_min, verbose=True)
    return model, optimizer, scheduler

# 학습 루프
def train_with_cutmix(model, loader, optimizer, scheduler, epochs, alpha, device, early_stopping, loss_path):
    model.train()

    os.makedirs(os.path.dirname(loss_path), exist_ok=True)

    if not os.path.exists(loss_path):
        with open(loss_path, 'w', newline='') as csvfile:
            fieldnames = ['epoch', 'loss', 'learning_rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(loss_path, 'a', newline='') as csvfile:
        fieldnames = ['epoch', 'loss', 'learning_rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for epoch in tqdm(range(epochs)):
            epoch_loss = 0
            for images in tqdm(loader):
                images = images.to(device)
                mixed_images, indices, lam = cutmix_data(images, alpha)
                p1, z1, p2, z2 = model(mixed_images, images)
                loss = simsiam_cutmix_loss_fn(p1, z1, p2, z2, indices, lam)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                scheduler.step(epoch + len(loader) / len(images))
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(loader)
            print(f"Epoch {epoch}, Average Loss: {avg_loss}")

            # CSV 파일에 에포크와 손실 값 추가
            writer.writerow({'epoch': epoch, 'loss': avg_loss, 'learning_rate': scheduler.get_last_lr()[0]})
            
            # Early stopping check
            early_stopping(avg_loss, model)
            if early_stopping.early_stop:
                print("Early stopping")
                break
    print("Training finished!")

if __name__ == "__main__":
    batch_size = 32
    lr = 0.001
    epochs = 10
    alpha = 1.0
    root_dir = './image'
    num_workers = 1
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dim = 512
    pred_dim = 128
    save_path='./best_model.pth'
    patience = 5
    min_delta = 0.01
    T_0 = 10
    T_mult = 1
    eta_min = 0
    loss_path = './loss_history.csv'

    # 이미지 증강을 위한 transform
    transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    base_encoder = models.efficientnet_b3(pretrained=True)

    loader = get_custom_data_loader(root_dir=root_dir, batch_size=batch_size, transform=transform, num_workers=num_workers)
    model, optimizer, scheduler = setup_model_and_optimizer(base_encoder=base_encoder, dim=dim, pred_dim=pred_dim, lr=lr, T_0=T_0, T_mult=T_mult, eta_min=eta_min)
    model = model.to(device)
    early_stopping = EarlyStopping(patience=patience, min_delta=min_delta, save_path=save_path)
    train_with_cutmix(model=model, loader=loader, optimizer=optimizer, scheduler=scheduler,
                      epochs=epochs, alpha=alpha, device=device, early_stopping=early_stopping, loss_path=loss_path)