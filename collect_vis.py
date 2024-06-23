import os
import shutil

target_labels_folder = "./datasets/VisDrone/AllLabels"
target_images_folder = "./datasets/VisDrone/AllImages"

train_labels_folder = "./datasets/VisDrone/VisDrone2019-DET-train/labels"
train_images_folder = "./datasets/VisDrone/VisDrone2019-DET-train/images"

val_images_folder = "./datasets/VisDrone/VisDrone2019-DET-val/images"
val_labels_folder = "./datasets/VisDrone/VisDrone2019-DET-val/labels"

train_labels = os.listdir(train_labels_folder)
train_images = os.listdir(train_images_folder)

val_labels = os.listdir(val_labels_folder)
val_images = os.listdir(val_images_folder)

print(len(val_labels))
print(len(val_images))

print(len(train_labels))
print(len(train_images))

for train_label in train_labels:
    source_label = os.path.join(train_labels_folder, train_label)
    destination_label = os.path.join(target_labels_folder, train_label)
    shutil.move(source_label, destination_label)

for train_image in train_images:
    source_image = os.path.join(train_images_folder, train_image)
    destination_image = os.path.join(target_images_folder, train_image)
    shutil.move(source_image, destination_image)

for val_label in val_labels:
    source_label = os.path.join(val_labels_folder, val_label)
    destination_label = os.path.join(target_labels_folder, val_label)
    shutil.move(source_label, destination_label)

for val_image in val_images:
    source_image = os.path.join(val_images_folder, val_image)
    destination_image = os.path.join(target_images_folder, val_image)
    shutil.move(source_image, destination_image)
