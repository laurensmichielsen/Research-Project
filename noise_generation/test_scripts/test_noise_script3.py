##### IMPORTANT: PATHS DEPEND ON LOCATION OF THE SCRIPT => FIGURE OUT BEFORE DELFTBLUE BY RUNNING SOME RANDOM SCRIPTS TO SEE
import generate_noise_type3
import os

labels_folder = './../data/PASCAL/labels/train/'
backup_labels_folder = './../data/PASCAL/noise3/'

generate_noise_type3.collect_labels_and_images(labels_folder, backup_labels_folder)

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
generate_noise_type3.generate_noise_type3(labels_folder, backup_labels_folder, 42)
generate_noise_type3.generate_noise_type3(labels_folder, backup_labels_folder, 23)
generate_noise_type3.generate_noise_type3(labels_folder, backup_labels_folder, 398)
generate_noise_type3.generate_noise_type3(labels_folder, backup_labels_folder, 445)
generate_noise_type3.generate_noise_type3(labels_folder, backup_labels_folder, 51)
# check if some annotations were altered
total_annotations_after_noise = 0
different_annotations = 0
for file in os.listdir(labels_folder):
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line != '':
                total_annotations_after_noise += 1
        actual_lines = labels[file]
        for line in lines:
            if line not in actual_lines:
                different_annotations += 1
print(total_annotations)
print(total_annotations_after_noise)
print(different_annotations)

generate_noise_type3.collect_labels_and_images(labels_folder, backup_labels_folder)

total_annotations_after_restore = 0
files_2 = os.listdir(labels_folder)
print(len(files_2))
for file in files_2:
    with open(os.path.join(labels_folder, file), 'r') as f:
        lines = f.readlines()
        total_annotations_after_restore += len(lines)
        assert labels[file] == lines
print(total_annotations_after_restore)