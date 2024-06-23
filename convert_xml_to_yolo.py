import xml.etree.ElementTree as ET
import os
import shutil

def convert_xml_to_yolo(xml_file_path, txt_file_path, class_dict):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Retrieve image dimensions
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    #create empty txt file
    open(txt_file_path, 'w').close()

    # Open the output file
    with open(txt_file_path, 'w') as file:
        # Iterate over each object in the XML
        for obj in root.iter('object'):
            class_name = obj.find('name').text
            # Convert class name to a class ID based on provided dictionary
            class_id = class_dict.get(class_name, -1)
            if class_id == -1:
                print(class_name)
                print('MISTAKEEE')
                continue  # Skip if class is not found

            # Parse bounding box coordinates
            bndbox = obj.find('bndbox')
            xmin = int(round(float(bndbox.find('xmin').text)))
            ymin = int(round(float(bndbox.find('ymin').text)))
            xmax = int(round(float(bndbox.find('xmax').text)))
            ymax = int(round(float(bndbox.find('ymax').text)))

            # Calculate YOLO format coordinates
            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            # Write to file
            file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

# Example usage

##classes  person
#• bird, cat, cow, dog, horse, sheep
#• aeroplane, bicycle, boat, bus, car, motorbike, train
#• bottle, chair, dining table, potted plant, sofa, tv/monitor
class_dict = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6,
              'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13,
              'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19}


# Loop through all the xml files in the directory:
files = os.listdir('./data/PASCAL/Annotations/')
print(len(files))
for file in files:
    if file.endswith('.xml'):

        xml_file_path = os.path.join('./data/PASCAL/Annotations/', file)
        txt_file_path = os.path.join('./data/PASCAL/AllLabels/', file.replace('.xml', '.txt'))
        convert_xml_to_yolo(xml_file_path, txt_file_path, class_dict)

# Split the data into train and validation

# train = []
# val = []
# for f in open('./data/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Main/train.txt'):
#     train.append(f.strip())

# for f in open('./data/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Main/val.txt'):
#     val.append(f.strip())

# # Move training labels and images to the train folder
# for name in train:
#     src_label = os.path.join('./data/VOC/AllLabels', name + '.txt')
#     dst_label = os.path.join('./data/VOC/train/labels', name + '.txt')
#     shutil.move(src_label, dst_label)
#     src_img = os.path.join('./data/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/JPEGImages', name + '.jpg')
#     dst_img = os.path.join('./data/VOC/train/images', name + '.jpg')
#     shutil.move(src_img, dst_img)

# # Move validation labels and images to the val folder
# for name in val:
#     src_label = os.path.join('./data/VOC/AllLabels', name + '.txt')
#     dst_label = os.path.join('./data/VOC/val/labels', name + '.txt')
#     shutil.move(src_label, dst_label)
#     src_img = os.path.join('./data/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/JPEGImages', name + '.jpg')
#     dst_img = os.path.join('./data/VOC/val/images', name + '.jpg')
#     shutil.move(src_img, dst_img)

# # Move remaining labels and images to the test folder
# for file in os.listdir('./data/VOC/AllLabels'):
#     src_label = os.path.join('./data/VOC/AllLabels', file)
#     dst_label = os.path.join('./data/VOC/test/labels', file)
#     shutil.move(src_label, dst_label)
#     src_img = os.path.join('./data/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/JPEGImages', file.replace('.txt', '.jpg'))
#     dst_img = os.path.join('./data/VOC/test/images', file.replace('.txt', '.jpg'))
#     shutil.move(src_img, dst_img)