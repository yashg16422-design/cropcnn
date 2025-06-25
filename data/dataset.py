import os
from PIL import Image
from torch.utils.data import Dataset

class CropDataset(Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.samples = []

        classes = sorted(os.listdir(root))
        self.class_to_idx = {c: i for i, c in enumerate(classes)}

        for c in classes:
            class_dir = os.path.join(root, c)
            for img in os.listdir(class_dir):
                self.samples.append((
                    os.path.join(class_dir, img),
                    self.class_to_idx[c]
                ))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label
