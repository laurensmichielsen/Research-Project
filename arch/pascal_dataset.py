import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

class_dict = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6,
              'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13,
              'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19, 'background': 20}

class Pascal(Dataset):
    def __init__(self, images, annotations, root_dir, root_dir_images, transform=None):
        # annotations: list of yolo annotation files -> which is labels folder in which it can be train/val/test subfolder
        self.annotations = annotations
        # root dir of the annotations
        self.root_dir = root_dir
        # transform to apply to the images
        self.transform = transform
        # class id dictionary
        self.class_id = class_dict
        # images: list of image files
        self.images = images
        # root dir of the images
        self.root_dir_images = root_dir_images
    
    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        img_name = self.images[idx]
        img_path = os.path.join(self.root_dir_images, img_name)
        image = Image.open(img_path)
        convert_tensor = transforms.ToTensor()
        image = convert_tensor(image)

        annotation_name = img_name.replace('.jpg', '.txt')
        annotation_path = os.path.join(self.root_dir, annotation_name)

        lines = []
        with open(annotation_path, 'r') as f:
            lines = f.readlines()
        
        boxes, labels, areas, iscrowd = [], [], [], []

        for line in lines:
            line = line.split()
            class_id = int(line[0])
            x_center = float(line[1])
            y_center = float(line[2])
            bbox_width = float(line[3])
            bbox_height = float(line[4])

            x_min = x_center - bbox_width/2
            y_min = y_center - bbox_height/2
            x_max = x_center + bbox_width/2
            y_max = y_center + bbox_height/2

            boxes.append([x_min, y_min, x_max, y_max])
            labels.append(class_id)
            areas.append(bbox_width * bbox_height)
            iscrowd.append(0)
        
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        areas = torch.as_tensor(areas, dtype=torch.float32)
        iscrowd = torch.as_tensor(iscrowd, dtype=torch.int64)

        target = {
            'boxes': boxes,
            'labels': labels,
            'image_id': torch.tensor([idx]),
            'area': areas,
            'iscrowd': iscrowd
        }

        if self.transform:
            image, target = self.transform(image, target)
        return image, target
