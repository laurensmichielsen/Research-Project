import generate_noise_type1
import os

# collect all the labels and create a dictionary with the file name linking to the lines in the file
labels_folder = './../data/PASCAL/labels/train/'
images_folder = './../data/PASCAL/images/train/'
backup_labels_folder = './../data/PASCAL/noise1/labels'
backup_images_folder = './../data/PASCAL/noise1/images'
seed = 1
labels = {}
total_annotations = 0
files = os.listdir(labels_folder)
print(len(files))
for file in files:
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        labels[file] = lines
        total_annotations += len(lines)

# Generate some noise
generate_noise_type1.generate_noise_type1(labels_folder, images_folder, backup_labels_folder, backup_images_folder, 2)
generate_noise_type1.generate_noise_type1(labels_folder, images_folder, backup_labels_folder, backup_images_folder, 3)

# check if some annotations were removed
total_annotations_after_noise = 0
for file in os.listdir(labels_folder):
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line != '':
                total_annotations_after_noise += 1
print(total_annotations)
print(total_annotations_after_noise)
# Restore the annotations
generate_noise_type1.collect_labels_and_images(labels_folder, images_folder, backup_labels_folder, backup_images_folder)

# check if the annotations are equal
total_annotations_after_restore = 0
files_2 = os.listdir(labels_folder)
print(len(files_2))
for file in files_2:
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        total_annotations_after_restore += len(lines)
        assert labels[file] == lines
print(total_annotations_after_restore)

