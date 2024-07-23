import torch.nn as nn
import torchvision.models as models

class SimSiam(nn.Module):
    def __init__(self, base_encoder, dim=2048, pred_dim=256):
        super(SimSiam, self).__init__()
        # Setup the encoder
        self.encoder = base_encoder
        self.encoder_dim = self.encoder.classifier[1].in_features  # EfficientNet의 경우 classifier[1]의 in_features 사용
        self.encoder.classifier = nn.Identity()  # Remove the classification head

        # Setup the projector
        self.projector = nn.Sequential(
            nn.Linear(self.encoder_dim, dim),
            nn.BatchNorm1d(dim),
            nn.ReLU(),
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim),
            nn.ReLU(),
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim)
        )

        # Setup the predictor
        self.predictor = nn.Sequential(
            nn.Linear(dim, pred_dim),
            nn.BatchNorm1d(pred_dim),
            nn.ReLU(),
            nn.Linear(pred_dim, dim)
        )

    def forward(self, x1, x2):
        z1 = self.projector(self.encoder(x1))
        z2 = self.projector(self.encoder(x2))

        p1 = self.predictor(z1)
        p2 = self.predictor(z2)

        return p1, z1, p2, z2

if __name__ == "__main__":
    base_encoder = models.efficientnet_b3(pretrained=True)
    model = SimSiam(base_encoder=base_encoder, dim=2048, pred_dim=256)
    print(model)