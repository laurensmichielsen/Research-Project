import os
import shutil

labels_folder = "./datasets/brain-tumor/AllLabels"
images_folder = "./datasets/brain-tumor/AllImages"

source_labels_folder = "./datasets/brain-tumor/train/labels"
source_images_folder = "./datasets/brain-tumor/train/images"

source_labels_folder_val = "./datasets/brain-tumor/valid/labels"
source_images_folder_val = "./datasets/brain-tumor/valid/images"

# Move all the labels and images to the labels and images folder

# labels = os.listdir(source_labels_folder)
# for label in labels:
#     shutil.move(os.path.join(source_labels_folder, label), os.path.join(labels_folder, label))
#     shutil.move(os.path.join(source_images_folder, label.replace("txt", "jpg")), os.path.join(images_folder, label.replace("txt", "jpg")))

# labels = os.listdir(source_labels_folder_val)
# for label in labels:
#     shutil.move(os.path.join(source_labels_folder_val, label), os.path.join(labels_folder, label))
#     shutil.move(os.path.join(source_images_folder_val, label.replace("txt", "jpg")), os.path.join(images_folder, label.replace("txt", "jpg")))

# Move all the images from the training folder to the AllImages folder
images = os.listdir(source_images_folder)
for image in images:
    shutil.move(os.path.join(source_images_folder, image), os.path.join(images_folder, image))