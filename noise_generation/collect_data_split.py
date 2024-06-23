import os
import shutil

def collect_to_all_labels_folder(labels_folder, train_folder):
    for label in os.listdir(train_folder):
        shutil.move(os.path.join(train_folder, label), os.path.join(labels_folder, label))

def collect_labels_and_images_type2_3_4_noise(original_labels_folder, original_target_labels_folder, labels_folder, target_labels_folder):
    # for now only collect training data but test and validation is very similar
    original_labels = os.listdir(original_labels_folder)
    target_labels = os.listdir(original_target_labels_folder)
    # pour original_labels and target_labels into a set
    original_labels_set = set(original_labels)
    target_labels_set = set(target_labels)
    labels = original_labels_set.union(target_labels_set)

    for label in labels:
        shutil.move(os.path.join(labels_folder, label), os.path.join(target_labels_folder, label))


def collect_labels_and_images_type1_noise(original_images_folder, original_target_images_folder, labels_folder, target_labels_folder, images_folder, target_images_folder):
    # original images and target folders is the folder from the result dir and from there we need to collect the images
    original_images = os.listdir(original_images_folder)
    original_target_images = os.listdir(original_target_images_folder)

    images = list(set(original_images).union(set(original_target_images)))

    for image in images:
        shutil.move(os.path.join(images_folder, image), os.path.join(target_images_folder, image))
        shutil.move(os.path.join(labels_folder, image.replace(".jpg", ".txt")), os.path.join(target_labels_folder, image.replace(".jpg", ".txt")))