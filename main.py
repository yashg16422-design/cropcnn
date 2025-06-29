import yaml
import torch
from torch.utils.data import DataLoader

from data.dataset import CropDataset
from data.transforms import build_transforms
from models.cnn import SimpleCNN
from training.trainer import Trainer
from training.evaluator import evaluate
from utils.logger import log

def main():
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using device: {device}")

    transforms = build_transforms(config["data"]["image_size"])
    dataset = CropDataset("data/images", transforms)

    train_size = int(len(dataset) * config["data"]["train_split"])
    val_size = len(dataset) - train_size
    train_set, val_set = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(
        train_set,
        batch_size=config["training"]["batch_size"],
        shuffle=True
    )

    val_loader = DataLoader(
        val_set,
        batch_size=config["training"]["batch_size"]
    )

    model = SimpleCNN(
        config["model"]["input_channels"],
        config["model"]["num_classes"]
    )

    trainer = Trainer(model, device, config["training"]["learning_rate"])

    for epoch in range(config["training"]["epochs"]):
        loss = trainer.train_epoch(train_loader)
        acc = evaluate(model, val_loader, device)
        log(f"Epoch {epoch+1}: loss={loss:.4f}, val_acc={acc:.4f}")

if __name__ == "__main__":
    main()
