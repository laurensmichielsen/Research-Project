import torch
import torchvision.transforms as T
from torch.utils.data import Dataset, random_split
from torchvision.datasets import VOCDetection
from typing import Callable, Optional
import torchvision.transforms as transforms
from PIL import Image

VOC_BBOX_LABEL_NAMES = (
    'background',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tvmonitor')

class PascalVOC(Dataset):
    def __init__(self, root: str, year: str = '2007', image_set: str = 'trainval', transform: Optional[Callable] = None):
        self.voc_dataset = VOCDetection(root=root, year=year, image_set=image_set, download=True)
        self.transform = transform

    def __len__(self):
        return len(self.voc_dataset)

    def resize_boxes(self, boxes, original_size, new_size):
        orig_width, orig_height = original_size
        new_width, new_height = new_size
        ratios = [new_width / orig_width, new_height / orig_height]
        new_boxes = []
        for box in boxes:
            resized_box = [
                box[0] * ratios[0],
                box[1] * ratios[1],
                box[2] * ratios[0],
                box[3] * ratios[1]
            ]
            new_boxes.append(resized_box)
        return new_boxes

    def __getitem__(self, idx):
        image, target = self.voc_dataset[idx]
        original_size = image.size
        convert_tensor = transforms.ToTensor()
        if self.transform is not None:
            img = self.transform(image)
        else:
            img = convert_tensor(image)

        new_size = (img.shape[-1], img.shape[-2])

        annotations = target['annotation']
        boxes = []
        labels = []
        for obj in annotations['object']:
            bbox = obj['bndbox']
            xmin = float(bbox['xmin'])
            xmax = float(bbox['xmax'])
            ymin = float(bbox['ymin'])
            ymax = float(bbox['ymax'])
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(VOC_BBOX_LABEL_NAMES.index(obj['name']))

        # Resize bounding boxes
        if transforms is not None:
            boxes = self.resize_boxes(boxes, original_size, new_size)

        target = {
            'boxes': torch.as_tensor(boxes, dtype=torch.float32),
            'labels': torch.as_tensor(labels, dtype=torch.int64),
            'image_id': torch.as_tensor(idx)
        }
        return img, target


    def get_train_val_test_datasets(self, seed, val_split=0.1, test_split=0.15):
        # Calculate sizes for train, validation, and test sets
        total_size = len(self)
        val_size = int(val_split * total_size)
        test_size = int(test_split * total_size)
        train_size = total_size - val_size - test_size
        
        # Use random_split to split the dataset
        generator = torch.Generator().manual_seed(seed)
        train_data, val_data, test_data = random_split(self, [train_size, val_size, test_size], generator=generator)
        
        return train_data, val_data, test_data

    
