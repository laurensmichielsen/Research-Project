# This script will corrupt 10% of the bounding box labels in the dataset
import random
import os
import shutil

def corrupt_bbox(class_id, x_center, y_center, bbox_width, bbox_height):
    # move the x_center and y_center by a random value between -0.1 and 0.1
    x_center_new = x_center + random.uniform(max(-0.1, - x_center), min(0.1, 1-x_center))
    y_center_new = y_center + random.uniform(max(-0.1, - y_center), min(0.1, 1-y_center))
    # generate new bbox_width and bbox_height
    max_width = min(1 - x_center_new, x_center_new) * 2
    max_height = min(1 - y_center_new, y_center_new) * 2
    max_width = min(1.1 * bbox_width, max_width)
    max_height = min(1.1 * bbox_height, max_height)
    bbox_width_new = random.uniform(0.9 * min(bbox_width, max_width), max_width)
    bbox_height_new = random.uniform(0.9 * min(bbox_height, max_height), max_height)
    return f'{class_id} {x_center_new} {y_center_new} {bbox_width_new} {bbox_height_new}\n'



def generate_noise_type3(labels_folder, target_labels_folder, seed, total_annotations=29969):
    num_annotations_to_corrupt = int(total_annotations * 0.1)
    print(num_annotations_to_corrupt)
    random.seed(seed)
    for i in range(0, num_annotations_to_corrupt):
        # get a random label file
        label_files = os.listdir(labels_folder)
        label_file = random.choice(label_files)
        # check if the file is already in the target_labels_folder
        check = os.path.exists(os.path.join(target_labels_folder, label_file))
        if not check:
            shutil.copy(os.path.join(labels_folder, label_file), os.path.join(target_labels_folder, label_file))
        # get the labels we can corrupt
        annotations = []
        with open(os.path.join(labels_folder, label_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                annotations.append(line)
        if not check:
            # choose any line to corrupt
            line_to_corrupt = random.choice(annotations)
            # corrupt the line 
            class_id, x_center, y_center, bbox_width, bbox_height = line_to_corrupt.split()
            # corrupt the bbox
            idx = annotations.index(line_to_corrupt)
            corrupted_line = corrupt_bbox(int(class_id), float(x_center), float(y_center), float(bbox_width), float(bbox_height))
            # remove the line_to_corrupt from the annotations
            annotations[idx] = corrupted_line
            # write the annotations back to the file
            with open(os.path.join(labels_folder, label_file), 'w') as f:
                for annotation in annotations:
                    f.write(annotation)
        else: 
            # collect the annotations from the target_labels_folder
            real_annotations = []
            with open(os.path.join(target_labels_folder, label_file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    real_annotations.append(line)
            # check if there are any annotations left to corrupt
            annotations_to_corrupt = []
            for annotation in annotations:
                if annotation in real_annotations:
                    annotations_to_corrupt.append(annotation)
            while len(annotations_to_corrupt) == 0:
                label_file = random.choice(label_files)
                annotations = []
                check = os.path.exists(os.path.join(target_labels_folder, label_file))
                if not check:
                    shutil.copy(os.path.join(labels_folder, label_file), os.path.join(target_labels_folder, label_file))
                with open(os.path.join(labels_folder, label_file), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        annotations.append(line)
                real_annotations = []
                with open(os.path.join(target_labels_folder, label_file), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        real_annotations.append(line)
                annotations_to_corrupt = []
                for annotation in annotations:
                    if annotation in real_annotations:
                        annotations_to_corrupt.append(annotation)
            # choose any line to corrupt
            line_to_corrupt = random.choice(annotations_to_corrupt)
            idx = annotations.index(line_to_corrupt)
            # corrupt the line
            class_id, x_center, y_center, bbox_width, bbox_height = line_to_corrupt.split()
            # corrupt the bbox
            corrupted_line = corrupt_bbox(int(class_id), float(x_center), float(y_center), float(bbox_width), float(bbox_height))
            # Update the annotation
            annotations[idx] = corrupted_line
            # write the annotations back to the file
            with open(os.path.join(labels_folder, label_file), 'w') as f:
                for annotation in annotations:
                    f.write(annotation)

def collect_labels_and_images(labels_folder, target_labels_folder):
    # target labels folder is the backup folder
    annotations = os.listdir(target_labels_folder)
    for annotation in annotations:
        # If the annotation is in the original folder, remove it
        os.remove(os.path.join(labels_folder, annotation))
        # Move the annotation back
        shutil.move(os.path.join(target_labels_folder, annotation), os.path.join(labels_folder, annotation))
