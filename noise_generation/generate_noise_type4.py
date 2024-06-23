import random
import os
import shutil

# Randomly perturbates the classes for 10% of the annotations
def generate_noise_type4(labels_folder, target_labels_folder, seed, total_annotations=29969):
    num_annotations_to_add = int(total_annotations * 0.1)
    random.seed(seed)
    for i in range(0, num_annotations_to_add):
        # get a random label file
        labels = os.listdir(labels_folder)
        label_file = random.choice(labels)
        # check if the file is already in the target_labels_folder
        if not os.path.exists(os.path.join(target_labels_folder, label_file)):
            shutil.copy(os.path.join(labels_folder, label_file), os.path.join(target_labels_folder, label_file))
        # open the file
        lines = []
        with open(os.path.join(labels_folder, label_file), 'r') as f:
            lines = f.readlines()
        # randomly perturbate one of the classes: 1. select a line 2. remove the line 3. select a new class, ensure it is different from the previous class
        # 4. write lines to the file
        # randomly select a annotation
        line_index = random.randint(0, len(lines) - 1)
        class_id, x_center, y_center, bbox_width, bbox_height = lines[line_index].split()
        # select a new class
        new_class_id = random.randint(0, 19)
        # ensure that the new class is different from the previous class
        while new_class_id == int(class_id):
            new_class_id = random.randint(0, 19)
        # write the new annotation
        lines[line_index] = f'{new_class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n'
        # write the new file
        with open(os.path.join(labels_folder, label_file), 'w') as f:
            f.writelines(lines)
    
def collect_labels_and_images(labels_folder, target_labels_folder):
    # target labels folder is the backup folder
    annotations = os.listdir(target_labels_folder)
    for annotation in annotations:
        # If the annotation is in the original folder, remove it
        os.remove(os.path.join(labels_folder, annotation))
        # Move the annotation back
        shutil.move(os.path.join(target_labels_folder, annotation), os.path.join(labels_folder, annotation))
        
    
