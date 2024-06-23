import random
import os
import shutil

# This method removes 10% of the annotations from the training set
def generate_noise_type1(labels_folder, images_folder, target_labels_folder, target_images_folder, seed, total_annotations=29969, image_suffix='.jpg'):
    # get the number of annotations to remove
    num_annotations_to_remove = int(total_annotations * 0.1)
    random.seed(seed)
    for i in range(0, num_annotations_to_remove):
        # get a random label file
        labels = os.listdir(labels_folder)
        label_file = random.choice(labels)
        if i % 1000 == 1:
            print(label_file)
        # check if the file is already in the target_labels_folder
        if not os.path.exists(os.path.join(target_labels_folder, label_file)):
            shutil.copy(os.path.join(labels_folder, label_file), os.path.join(target_labels_folder, label_file))
        # open the file
        lines = []
        with open(os.path.join(labels_folder, label_file), 'r') as f:
            lines = f.readlines()
        # remove a random line from the file
        lines.pop(random.randint(0, len(lines) - 1))
        # if there are no more annotations left in the file, move the corresponding image to the target_images_folder and 
        # don't keep the image in the target_labels_folder and remove the annotations file
        if len(lines) == 0:
            shutil.move(os.path.join(images_folder, os.path.splitext(label_file)[0] + image_suffix), os.path.join(target_images_folder, os.path.splitext(label_file)[0] + image_suffix))
            os.remove(os.path.join(labels_folder, label_file))
        else:            
            # write the new file
            with open(os.path.join(labels_folder, label_file), 'w') as f:
                f.writelines(lines)
        # if i % 1000 == 1:
        #     # fetch the file and print the lines
        #     if os.path.exists(os.path.join(labels_folder, label_file)):
        #         with open(os.path.join(labels_folder, label_file), 'r') as f:
        #             lines = f.readlines()
        #             print(lines)

# This method restores the annotations that were removed in the previous method and moves the images that had no annotations back to the original folder
def collect_labels_and_images(labels_folder, images_folder, target_labels_folder, target_images_folder):
    # target labels folder is the backup folder
    annotations = os.listdir(target_labels_folder)
    for annotation in annotations:
        # If the annotation is in the original folder, remove it
        if os.path.exists(os.path.join(labels_folder, annotation)):
            os.remove(os.path.join(labels_folder, annotation))
        # Move the annotation back
        shutil.move(os.path.join(target_labels_folder, annotation), os.path.join(labels_folder, annotation))
    images = os.listdir(target_images_folder)
    for image in images:
        # move the image back
        shutil.move(os.path.join(target_images_folder, image), os.path.join(images_folder, image))
