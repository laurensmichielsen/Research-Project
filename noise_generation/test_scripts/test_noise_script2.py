import generate_noise_type2
import os

labels_folder = './../data/PASCAL/labels/train/'
backup_labels_folder = './../data/PASCAL/noise2/'

labels = {}
total_annotations = 0
files = os.listdir(labels_folder)
print(len(files))
for file in files:
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        labels[file] = lines
        total_annotations += len(lines)

# Generate noise of type 2
generate_noise_type2.generate_noise_type2(labels_folder, backup_labels_folder, 999)
generate_noise_type2.generate_noise_type2(labels_folder, backup_labels_folder, 1000)
generate_noise_type2.generate_noise_type2(labels_folder, backup_labels_folder, 1001)
generate_noise_type2.generate_noise_type2(labels_folder, backup_labels_folder, 1002)
generate_noise_type2.generate_noise_type2(labels_folder, backup_labels_folder, 1003)
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

generate_noise_type2.collect_labels_and_images(labels_folder, backup_labels_folder)

total_annotations_after_restore = 0
files_2 = os.listdir(labels_folder)
print(len(files_2))
for file in files_2:
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        total_annotations_after_restore += len(lines)
        assert labels[file] == lines
print(total_annotations_after_restore)
