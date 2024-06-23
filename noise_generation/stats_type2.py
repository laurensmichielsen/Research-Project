import os
import random
from generate_noise_type2v2 import generate_noise_type2, collect_labels_and_images
import json
import statistics
import collect_data_split as split
import shutil

def write_stats_to_file(file_name, noise_level, annotations_per_class_this_run, areas_this_run, highest_IoU_this_run, original_annotations_per_image_this_run, annotations_before_this_run,
                        annotations_per_class, areas, highest_IoU, original_annotations_per_image):
    print(f"Writing stats to file for noise level {noise_level}")
    # calculate the mean, stdev, and quantiles of the areas_this_run
    mean_areas_this_run = statistics.mean(areas_this_run)
    stdev_areas_this_run = statistics.stdev(areas_this_run)
    quantiles_areas_this_run = statistics.quantiles(areas_this_run, n=4)
    # calculate the mean, stdev, and quantiles of the highest_IoU_this_run
    mean_highest_IoU_this_run = statistics.mean(highest_IoU_this_run)
    stdev_highest_IoU_this_run = statistics.stdev(highest_IoU_this_run)
    quantiles_highest_IoU_this_run = statistics.quantiles(highest_IoU_this_run, n=4)
    # calculate the mean, stdev, and quantiles of the original_annotations_per_image_this_run
    mean_original_annotations_per_image_this_run = statistics.mean(original_annotations_per_image_this_run)
    stdev_original_annotations_per_image_this_run = statistics.stdev(original_annotations_per_image_this_run)
    quantiles_original_annotations_per_image_this_run = statistics.quantiles(original_annotations_per_image_this_run, n=4)
    # calculate the median, stdev, and quantiles of the annotations_before_this_run
    mean_annotations_before_this_run = statistics.mean(annotations_before_this_run)
    stdev_annotations_before_this_run = statistics.stdev(annotations_before_this_run)
    quantiles_annotations_before_this_run = statistics.quantiles(annotations_before_this_run, n=4)
    # calculate the median, stdev, and quantiles of areas
    mean_areas = statistics.mean(areas)
    stdev_areas = statistics.stdev(areas)
    quantiles_areas = statistics.quantiles(areas, n=4)
    # calculate the median, stdev, and quantiles of highest_IoU
    mean_highest_IoU = statistics.mean(highest_IoU)
    stdev_highest_IoU = statistics.stdev(highest_IoU)
    quantiles_highest_IoU = statistics.quantiles(highest_IoU, n=4)
    # calculate the median, stdev, and quantiles of original_annotations_per_image
    mean_original_annotations_per_image = statistics.mean(original_annotations_per_image)
    stdev_original_annotations_per_image = statistics.stdev(original_annotations_per_image)
    quantiles_original_annotations_per_image = statistics.quantiles(original_annotations_per_image, n=4)

    data = {
        "noise_level": noise_level,
        "annotations_per_class_this_run": annotations_per_class_this_run,
        "areas_this_run" : {
            "mean": mean_areas_this_run,
            "stdev": stdev_areas_this_run,
            "quantiles": quantiles_areas_this_run
        },
        "highest_IoU_this_run": {
            "mean": mean_highest_IoU_this_run,
            "stdev": stdev_highest_IoU_this_run,
            "quantiles": quantiles_highest_IoU_this_run
        },
        "original_annotations_per_image_this_run": {
            "mean": mean_original_annotations_per_image_this_run,
            "stdev": stdev_original_annotations_per_image_this_run,
            "quantiles": quantiles_original_annotations_per_image_this_run
        },
        "annotations_before_this_run": {
            "mean": mean_annotations_before_this_run,
            "stdev": stdev_annotations_before_this_run,
            "quantiles": quantiles_annotations_before_this_run
        },
        "annotations_per_class": annotations_per_class,
        "areas": {
            "mean": mean_areas,
            "stdev": stdev_areas,
            "quantiles": quantiles_areas
        },
        "highest_IoU": {
            "mean": mean_highest_IoU,
            "stdev": stdev_highest_IoU,
            "quantiles": quantiles_highest_IoU
        },
        "original_annotations_per_image": {
            "mean": mean_original_annotations_per_image,
            "stdev": stdev_original_annotations_per_image,
            "quantiles": quantiles_original_annotations_per_image
        },
    }
    # Open the JSON file in read mode
    try:
        with open(file_name, 'r') as json_file:
            # Load existing data from the JSON file
            try:
                # Load existing data from the JSON file
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                # If the file is empty or contains invalid JSON, initialize with an empty list
                existing_data = []
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty list
        existing_data = []

    # Append new data to the existing list
    existing_data.append(data)

    # Open the JSON file in write mode
    with open(file_name, 'w') as json_file:
        # Write the updated list of data objects to the JSON file
        json.dump(existing_data, json_file, indent=4)


def calc_highest_IoU(x_center, y_center, bbox_width, bbox_height, original_lines):
    IoUs = []
    for line in original_lines:
        class_id, x_center_original, y_center_original, bbox_width_original, bbox_height_original = line.split()
        x_center_original = float(x_center_original)
        y_center_original = float(y_center_original)
        bbox_width_original = float(bbox_width_original)
        bbox_height_original = float(bbox_height_original)
        # calculate the intersection
        x1 = max(x_center - bbox_width / 2, x_center_original - bbox_width_original / 2)
        y1 = max(y_center - bbox_height / 2, y_center_original - bbox_height_original / 2)
        x2 = min(x_center + bbox_width / 2, x_center_original + bbox_width_original / 2)
        y2 = min(y_center + bbox_height / 2, y_center_original + bbox_height_original / 2)
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        # calculate the union
        union = bbox_width * bbox_height + bbox_width_original * bbox_height_original - intersection
        IoU = intersection / union if union != 0 else 0
        IoUs.append(IoU)
    return max(IoUs) if IoUs else 0

def generate_statistics_type2(labels_folder, target_labels_folder, seeds, file_name, number_of_classes=20):
    # Initialize the dictionary that will store the annotations that were added per file
    original_label_files = os.listdir(labels_folder)
    annotations_added_dict = {}
    for label_file in original_label_files:
        annotations_added_dict[label_file] = []
    # Initialize the array that will store the number of annotations that were added per class
    annotations_per_class = [0] * number_of_classes
    # Initialize the array that will store the areas of the added annotations
    areas = []
    # Initialize the array that will store the highest IoU of the added annotations with the original annotations
    highest_IoU = []
    # Initialize the array that will store the original number of annotations per image
    original_annotations_per_image = []

    for noise_level in range(0, len(seeds)):
        # Generate the noise
        generate_noise_type2(labels_folder, target_labels_folder, seeds[noise_level])
        print(f"Generated noise for noise level {noise_level}")
        # initialize the ds for the stats of this run
        annotations_per_class_this_run = [0] * number_of_classes
        areas_this_run = []
        highest_IoU_this_run = []
        original_annotations_per_image_this_run = []
        annotations_before_this_run = []
        # collect the labels that are in the target_labels_folder as they correspond to the label files in the label_folder that have added annotations
        labels_with_added_annotations = os.listdir(target_labels_folder)
        for label_file in labels_with_added_annotations:
            # get the original annotations from the file in target_labels_folder
            original_lines = []
            with open(os.path.join(target_labels_folder, label_file), 'r') as f:
                original_lines = f.readlines()
            # get the corrupted lines from the file in labels_folder
            corrupted_lines = []
            with open(os.path.join(labels_folder, label_file), 'r') as f:
                corrupted_lines = f.readlines()
            # get the annotations that were added
            added_annotations = list(set(corrupted_lines) - set(original_lines))
            # get the annotations that were added this run
            added_annotations_this_run = list(set(added_annotations) - set(annotations_added_dict[label_file]))

            for line in added_annotations_this_run:
                class_id, x_center, y_center, bbox_width, bbox_height = line.split()
                annotations_per_class_this_run[int(class_id)] += 1
                areas_this_run.append(float(bbox_width) * float(bbox_height))
                highest_IoU_this_run.append(calc_highest_IoU(float(x_center), float(y_center), float(bbox_width), float(bbox_height), original_lines))
                original_annotations_per_image_this_run.append(len(original_lines))
                annotations_before_this_run.append(len(corrupted_lines) - len(added_annotations_this_run))

            annotations_added_dict[label_file] += added_annotations_this_run
        # calculate the statistics thus far
        for i in range(0, number_of_classes):
            annotations_per_class[i] += annotations_per_class_this_run[i]
        # append the areas of the added annotations
        areas.extend(areas_this_run)
        # append the highest IoU of the added annotations with the original annotations
        highest_IoU.extend(highest_IoU_this_run)
        # append the original number of annotations per image
        original_annotations_per_image.extend(original_annotations_per_image_this_run)

        write_stats_to_file(file_name, noise_level, annotations_per_class_this_run, areas_this_run, highest_IoU_this_run, original_annotations_per_image_this_run, annotations_before_this_run,
                            annotations_per_class, areas, highest_IoU, original_annotations_per_image)

    collect_labels_and_images(labels_folder, target_labels_folder)

label_folder = "./../data/PASCAL/labels/train"
target_label_folder = "./../data/PASCAL/noise2"
seeds = [14, 15, 16, 17, 18]

file_name = "./exp2v2_stats_run1.json"

all_labels_folder = "./../datasets/VisDrone/AllLabels"
#original_labels_folder = "./../../results/exp2/exp2_run_2_4/Research/data/PASCAL/labels/train"
#original_target_labels_folder = "./../../results/exp2/exp2_run_2_4/Research/data/PASCAL/noise2"


#split.collect_labels_and_images_type2_3_4_noise(original_labels_folder, original_target_labels_folder, all_labels_folder, label_folder)
print("Stats")

generate_statistics_type2(label_folder, target_label_folder, seeds, file_name)
collect_labels_and_images(label_folder, target_label_folder)