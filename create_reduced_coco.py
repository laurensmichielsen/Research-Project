import os
import shutil

train_labels_folder = "./dataset2/TrainLabels"
val_labels_folder = "./dataset2/ValLabels"

train_images_folder = "./dataset2/train2017/train2017"
val_images_folder = "./dataset2/val2017/val2017"

target_label_folder = "./dataset2/AllLabels"
target_image_folder = "./dataset2/AllImages"

ids_to_keep = [75, 74, 72, 71, 70, 69, 68, 67, 60, 57, 56, 45, 44, 43, 42, 41, 40, 39]

train_labels = os.listdir(train_labels_folder)

for label in train_labels:
    lines = []
    with open(os.path.join(train_labels_folder, label), "r") as f:
        lines = f.readlines()

    # Check if it contains an annotation that is not in the ids_to_keep list
    keep = True
    for line in lines:
        class_id = int(line.split()[0])
        if class_id not in ids_to_keep:
            keep = False
            break
    
    # if the label contains only the ids_to_keep, keep it else we remove it
    if not keep:
        os.remove(os.path.join(train_labels_folder, label))
        os.remove(os.path.join(train_images_folder, label.replace(".txt", ".jpg")))

print(f"Recuded train labels: {len(os.listdir(train_labels_folder))}")
print(f"Recuded train images: {len(os.listdir(train_images_folder))}")

val_labels = os.listdir(val_labels_folder)

for label in val_labels:
    lines = []
    with open(os.path.join(val_labels_folder, label), "r") as f:
        lines = f.readlines()

    # Check if it contains an annotation that is not in the ids_to_keep list
    keep = True
    for line in lines:
        class_id = int(line.split()[0])
        if class_id not in ids_to_keep:
            keep = False
            break
    
    # if the label contains only the ids_to_keep, keep it else we remove it
    if not keep:
        os.remove(os.path.join(val_labels_folder, label))
        os.remove(os.path.join(val_images_folder, label.replace(".txt", ".jpg")))

print(f"Recuded val labels: {len(os.listdir(val_labels_folder))}")
print(f"Recuded val images: {len(os.listdir(val_images_folder))}")

# Remove the images that don't have a corresponding label
train_labels = os.listdir(train_labels_folder)
train_images = os.listdir(train_images_folder)

for image in train_images:
    if image.replace(".jpg", ".txt") not in train_labels:
        os.remove(os.path.join(train_images_folder, image))

print(f"Recuded train images: {len(os.listdir(train_images_folder))}")
print(f"Recuded train labels: {len(os.listdir(train_labels_folder))}")

val_labels = os.listdir(val_labels_folder)
val_images = os.listdir(val_images_folder)

for image in val_images:
    if image.replace(".jpg", ".txt") not in val_labels:
        os.remove(os.path.join(val_images_folder, image))

print(f"Recuded val images: {len(os.listdir(val_images_folder))}")
print(f"Recuded val labels: {len(os.listdir(val_labels_folder))}")

# Move all the labels to the target label folder
train_labels = os.listdir(train_labels_folder)
val_labels = os.listdir(val_labels_folder)

for label in train_labels:
    shutil.move(os.path.join(train_labels_folder, label), os.path.join(target_label_folder, label))

for label in val_labels:
    shutil.move(os.path.join(val_labels_folder, label), os.path.join(target_label_folder, label))

# Move all the images to the target image folder
train_images = os.listdir(train_images_folder)
val_images = os.listdir(val_images_folder)

for image in train_images:
    shutil.move(os.path.join(train_images_folder, image), os.path.join(target_image_folder, image))

for image in val_images:
    shutil.move(os.path.join(val_images_folder, image), os.path.join(target_image_folder, image))
