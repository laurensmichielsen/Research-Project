import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
import xml.etree.ElementTree as ET

class_dict = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6,
              'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13,
              'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19, 'background': 20}

class Pascal(Dataset):
    def __init__(self, images, annotations, root_dir, root_dir_images, transform=None):
        # List of image files
        self.images = images
        # List of annotation files
        self.annotations = annotations
        # Root directory of the annotations
        self.root_dir = root_dir
        # Root directory of the images
        self.root_dir_images = root_dir_images
        # Transform to apply to the images
        self.transform = transform
        # Class id dictionary
        self.class_id = class_dict

    def __len__(self):
        return len(self.images)

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
        img_name = self.images[idx]
        img_path = os.path.join(self.root_dir_images, img_name)
        image = Image.open(img_path).convert("RGB")
        original_size = image.size

        annotation_name = self.annotations[idx]
        annotation_path = os.path.join(self.root_dir, annotation_name)
        tree = ET.parse(annotation_path)
        root = tree.getroot()

        boxes = []
        labels = []
        for obj in root.findall('object'):
            label = obj.find('name').text
            if label in self.class_id:
                bbox = obj.find('bndbox')
                x_min = float(bbox.find('xmin').text)
                y_min = float(bbox.find('ymin').text)
                x_max = float(bbox.find('xmax').text)
                y_max = float(bbox.find('ymax').text)
                boxes.append([x_min, y_min, x_max, y_max])
                labels.append(self.class_id[label])

        if self.transform is not None:
            image = self.transform(image)
        
        new_size = (image.shape[-1], image.shape[-2])

        if self.transform is not None:
            boxes = self.resize_boxes(boxes, original_size, new_size)

        target = {
            'boxes': torch.tensor(boxes, dtype=torch.float32),
            'labels': torch.tensor(labels, dtype=torch.int64),
            'image_id': torch.tensor([idx]),
        }

        return image, target

# import os
# import torch
# from torch.utils.data import Dataset
# from PIL import Image
# from torchvision import transforms

# class_dict = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6,
#               'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13,
#               'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19, 'background': 20}


# class Pascal(Dataset):
#     def __init__(self, images, annotations, root_dir, root_dir_images, transform=None):
#         # annotations: list of yolo annotation files -> which is labels folder in which it can be train/val/test subfolder
#         self.annotations = annotations
#         # root dir of the annotations
#         self.root_dir = root_dir
#         # transform to apply to the images
#         self.transform = transform
#         # class id dictionary
#         self.class_id = class_dict
#         # images: list of image files
#         self.images = images
#         # root dir of the images
#         self.root_dir_images = root_dir_images

#     def __len__(self):
#         return len(self.images)

#     def resize_boxes(self, boxes, original_size, new_size):
#         orig_width, orig_height = original_size
#         new_width, new_height = new_size
#         ratios = [new_width / orig_width, new_height / orig_height]
#         new_boxes = []
#         for box in boxes:
#             resized_box = [
#                 box[0] * ratios[0],
#                 box[1] * ratios[1],
#                 box[2] * ratios[0],
#                 box[3] * ratios[1]
#             ]
#             new_boxes.append(resized_box)
#         return new_boxes


#     def __getitem__(self, idx):
#         img_name = self.images[idx]
#         img_path = os.path.join(self.root_dir_images, img_name)
#         image = Image.open(img_path)
#         convert_tensor = transforms.ToTensor()

#         if self.transform is not None:
#             image = self.transform(image)
#         else:
#             image = convert_tensor(image)

#         new_size = (image.shape[-1], image.shape[-2])

#         target = self.get_target(idx)

#         annotation_name = annotations[idx]
#         annotation_path = os.path.join(self.root_dir, annotation_name)
#         tree = ET.parse(annotation_path)

#         annotations = tree['annotation']
#         boxes = []
#         labels = []
#         for obj in annotations['object']:
#             bbox = obj['bndbox']
#             x_min = float(bbox['xmin'])
#             y_min = float(bbox['ymin'])
#             x_max = float(bbox['xmax'])
#             y_max = float(bbox['ymax'])

#             boxes.append([x_min, y_min, x_max, y_max])
#             labels.append(self.class_id[obj['name']])

#         if transforms is not None:
#             boxes = self.resize_boxes(boxes, original_size, new_size)

#         target = {
#             'boxes': torch.tensor(boxes, dtype=torch.float32),
#             'labels': torch.tensor(labels, dtype=torch.int64),
#             'image_id': torch.tensor([idx]),
#         }
#         return img, target
        