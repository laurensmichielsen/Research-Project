# This script splits the images and labels into train, validation, and test folders.
import os
import torch
import shutil

train_percentage = 0.75
val_percentage = 0.1
test_percentage = 0.15

def create_data_split(images_folder, labels_folder, target_images_folder, target_labels_folder, seed, image_suffix='.jpg'):
    # get all the file names
    files = os.listdir(images_folder)
    # remove the file extension
    files = [os.path.splitext(file)[0] for file in files]
    torch.manual_seed(seed)
    # make a random permutation of the file names
    permuted_files = torch.randperm(len(files))
    files = [files[i] for i in permuted_files]
    # split the data
    train = files[:int(len(files) * train_percentage)]
    val = files[int(len(files) * train_percentage):int(len(files) * (train_percentage + val_percentage))]
    test = files[int(len(files) * (train_percentage + val_percentage)):]

    # Move training labels and images to the train folder
    for name in train:
        # move the labels to the labels folder
        label_name = name + '.txt'
        destination_label = os.path.join(target_labels_folder, 'train', label_name)
        source_label = os.path.join(labels_folder, label_name)
        # check if the source label exists
        if os.path.exists(source_label):
            shutil.move(source_label, destination_label)

        # move the images to the images folder
        image_name = name + image_suffix
        destination_image = os.path.join(target_images_folder, 'train', image_name)
        source_image = os.path.join(images_folder, image_name)
        shutil.move(source_image, destination_image)

    # Move validation labels and images to the val folder
    for name in val:
        # move the labels to the labels folder
        label_name = name + '.txt'
        destination_label = os.path.join(target_labels_folder, 'val', label_name)
        source_label = os.path.join(labels_folder, label_name)
        # check if the source label exists
        if os.path.exists(source_label):
            shutil.move(source_label, destination_label)

        # move the images to the images folder
        image_name = name + image_suffix
        destination_image = os.path.join(target_images_folder, 'val', image_name)
        source_image = os.path.join(images_folder, image_name)
        shutil.move(source_image, destination_image)

    # Move test labels and images to the test folder
    for name in test:
        # move the labels to the labels folder
        label_name = name + '.txt'
        destination_label = os.path.join(target_labels_folder, 'test', label_name)
        source_label = os.path.join(labels_folder, label_name)
        # check if the source label exists
        if os.path.exists(source_label):
            shutil.move(source_label, destination_label)

        # move the images to the images folder
        image_name = name + image_suffix
        destination_image = os.path.join(target_images_folder, 'test', image_name)
        source_image = os.path.join(images_folder, image_name)
        shutil.move(source_image, destination_image)

def collect_labels_and_images(images_folder, labels_folder, target_images_folder, target_labels_folder):
    # get the images and labels from the train, test, and val folders back to the original folders
    for folder in ['train', 'val', 'test']:
        for file in os.listdir(os.path.join(target_labels_folder, folder)):
            source_label = os.path.join(target_labels_folder, folder, file)
            destination_label = os.path.join(labels_folder, file)
            shutil.move(source_label, destination_label)

            image_name = file.replace('.txt', '.jpg')
            source_image = os.path.join(target_images_folder, folder, image_name)
            destination_image = os.path.join(images_folder, image_name)
            shutil.move(source_image, destination_image)
        # move the images without a label back
        for file in os.listdir(os.path.join(target_images_folder, folder)):
            image_name = file
            source_image = os.path.join(target_images_folder, folder, image_name)
            destination_image = os.path.join(images_folder, image_name)
            shutil.move(source_image, destination_image)

#collect_labels_and_images(images_folder, labels_folder, target_images_folder, target_labels_folder)
# create_data_split(images_folder, labels_folder, target_images_folder, target_labels_folder, 12, image_suffix='.jpg')
# images_folder = './datasets/VisDrone/AllImages/'
# labels_folder = './datasets/VisDrone/AllLabels/'
# # target folders for images and labels
# target_images_folder = './datasets/VisDrone/images/'
# target_labels_folder = './datasets/VisDrone/labels/'

# images_folder = "./data2/PASCAL/AllImages/"
# labels_folder = "./data2/PASCAL/AllLabels/"
# # target folders for images and labels
# target_images_folder = "./data2/PASCAL/images/"
# target_labels_folder = "./data2/PASCAL/labels/"

images_folder = "./datasets/brain-tumor/AllImages/"
labels_folder = "./datasets/brain-tumor/AllLabels/"
# target folders for images and labels
target_images_folder = "./datasets/brain-tumor/images/"
target_labels_folder = "./datasets/brain-tumor/labels/"

collect_labels_and_images(images_folder, labels_folder, target_images_folder, target_labels_folder)
# create_data_split(images_folder, labels_folder, target_images_folder, target_labels_folder, 42, image_suffix='.jpg')
# collect_labels_and_images(images_folder, labels_folder, target_images_folder, target_labels_folder)