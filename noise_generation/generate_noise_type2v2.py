import random
import os
import shutil
import numpy as np

number_of_classes = 20
def create_annotation(centers, epsilon=0.0005):
    # generate a new x_center, and y_center
    x_center = np.random.normal(0.5, 0.185)
    y_center = np.random.normal(0.5, 0.185)
    #x_center = random.uniform(0, 1)
    #y_center = random.uniform(0, 1)
    # ensure that the distance between the new center and the existing centers is at least epsilon
    min_distance = 2
    for center in centers:
        distance = ((center[0] - x_center) ** 2 + (center[1] - y_center) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
    while min_distance < epsilon or (x_center < 0 or x_center > 1 or y_center < 0 or y_center > 1):
        print('')
        min_distance = 2
        x_center = np.random.normal(0.5, 0.185)
        y_center = np.random.normal(0.5, 0.185)
        print(x_center, y_center)
        #x_center = random.uniform(0, 1)
        #y_center = random.uniform(0, 1)
        for center in centers:
            distance = ((center[0] - x_center) ** 2 + (center[1] - y_center) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
    # generate a new bbox_width and bbox_height
    width_range = min(1 - x_center, x_center) * 2
    height_range = min(1 - y_center, y_center) * 2
    bbox_width = random.uniform(width_range * 0.5, width_range)
    bbox_height = random.uniform(height_range * 0.5, height_range)
    # Generate a random class_id: 0 or 1 or 2 or ... or 19
    class_id = random.randint(0, number_of_classes - 1)
    assert x_center >= 0 and x_center <= 1
    return class_id, x_center, y_center, bbox_width, bbox_height

# Type 2: Extra annotations are added to the training set
# This method adds 10% of the annotations to the training set
def generate_noise_type2(labels_folder, target_labels_folder, seed, total_annotations=29969):
    num_annotations_to_add = int(total_annotations * 0.1)
    random.seed(seed)
    for i in range(0, num_annotations_to_add):
        # get a random label file
        labels = os.listdir(labels_folder)
        label_file = random.choice(labels)
        # check if the file is already in the target_labels_folder
        if not os.path.exists(os.path.join(target_labels_folder, label_file)):
            shutil.copy(os.path.join(labels_folder, label_file), os.path.join(target_labels_folder, label_file))
        # collect the centers of the bounding boxes
        centers = []
        with open(os.path.join(labels_folder, label_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                class_id, x_center, y_center, bbox_width, bbox_height = line.split()
                centers.append((float(x_center), float(y_center)))
        # create a new annotation
        class_id, x_center, y_center, bbox_width, bbox_height = create_annotation(centers)
        with open(os.path.join(labels_folder, label_file), 'a') as f:
            f.write(f'{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n')
        
def collect_labels_and_images(labels_folder, target_labels_folder):
    # target labels folder is the backup folder
    annotations = os.listdir(target_labels_folder)
    print(len(annotations))
    for annotation in annotations:
        # If the annotation is in the original folder, remove it
        os.remove(os.path.join(labels_folder, annotation))
        # Move the annotation back
        shutil.move(os.path.join(target_labels_folder, annotation), os.path.join(labels_folder, annotation))

