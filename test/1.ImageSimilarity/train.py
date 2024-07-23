import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import torchvision.models as models
import os
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
from model import SimSiam

# SimSiam 클래스 정의 (위에서 이미 제공된 코드와 같이 정의해야 합니다.)

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
    cut_w = np.int(W * cut_rat)
    cut_h = np.int(H * cut_rat)

    cx = np.random.randint(W)
    cy = np.random.randint(H)

    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bby2 = np.clip(cy + cut_h // 2, 0, H)

    return bbx1, bby1, bbx2, bby2

def loss_fn(p, z, index, lam):
    """Calculate loss for CutMix-augmented batch."""
    z = z.detach()  # Stop gradient
    p = nn.functional.normalize(p, dim=1)
    z = nn.functional.normalize(z, dim=1)
    return -((lam * (p * z).sum(dim=1) + (1 - lam) * (p * z[index]).sum(dim=1)).mean())

# Custom Dataset
class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): 이미지 파일이 저장된 디렉토리 경로.
            transform (callable, optional): 이미지에 적용할 변형(transform).
        """
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

# 이미지 증강을 위한 transform
transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 모델 및 최적화 설정
def setup_model_and_optimizer(base_encoder, dim, pred_dim, lr):
    model = SimSiam(base_encoder=base_encoder, dim=dim, pred_dim=pred_dim)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    return model, optimizer

# 학습 루프
def train_with_cutmix(model, loader, optimizer, epochs, alpha, device):
    model.train()
    for epoch in range(epochs):
        for images in loader:
            images = images.to(device)
            mixed_images, indices, lam = cutmix_data(images, alpha)
            p1, p2 = model(mixed_images, images)
            loss = loss_fn(p1, p2, indices, lam)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch}, Loss: {loss.item()}")
    print("Training finished!")

if __name__ == "__main__": 
    batch_size = 64
    lr = 0.001
    epochs = 10
    alpha = 1.0
    root_dir = './image'
    num_workers = 1
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dim = 2048
    pred_dim = 256

    loader = get_custom_data_loader(root_dir=root_dir, batch_size=batch_size, transform=transform, num_workers=num_workers)
    model, optimizer = setup_model_and_optimizer(base_encoder=models.resnet50(pretrained=True), dim=dim, pred_dim=pred_dim, lr = lr)
    train_with_cutmix(model=model, loader=loader, optimizer=optimizer, epochs=epochs, alpha=alpha, device=device)