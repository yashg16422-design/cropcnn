import torch
from torch.nn import CrossEntropyLoss
from torch.optim import Adam

class Trainer:
    def __init__(self, model, device, lr):
        self.model = model.to(device)
        self.device = device
        self.criterion = CrossEntropyLoss()
        self.optimizer = Adam(model.parameters(), lr=lr)

    def train_epoch(self, loader):
        self.model.train()
        total_loss = 0.0

        for images, labels in loader:
            images = images.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(loader)
