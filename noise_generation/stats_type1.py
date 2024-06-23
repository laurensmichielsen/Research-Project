import os
from generate_noise_type1 import generate_noise_type1, collect_labels_and_images
import statistics
import json

import collect_data_split as split

def calculate_and_write_stats(file_name, noise_level, annotations_removed_per_class_this_run, areas_removed_this_run, original_annotations_this_run,
        annotations_removed_per_class, areas_removed, original_annotations, num_of_classes=20):
    
    # Calculate the stats for this run
    # calculate the mean, stdev, quantiles for areas_removed_this_run
    mean_area_removed_this_run = statistics.mean(areas_removed_this_run)
    stdev_area_removed_this_run = statistics.stdev(areas_removed_this_run)
    quantiles_area_removed_this_run = statistics.quantiles(areas_removed_this_run, n=4)
    # calculate the mean, stdev, quantiles for original_annotations_this_run
    mean_original_annotations_this_run = statistics.mean(original_annotations_this_run)
    stdev_original_annotations_this_run = statistics.stdev(original_annotations_this_run)
    quantiles_original_annotations_this_run = statistics.quantiles(original_annotations_this_run, n=4)
    # calculate the mean, stdev, quantiles for areas_removed
    mean_area_removed = statistics.mean(areas_removed)
    stdev_area_removed = statistics.stdev(areas_removed)
    quantiles_area_removed = statistics.quantiles(areas_removed, n=4)
    # calculate the mean, stdev, quantiles for original_annotations
    mean_original_annotations = statistics.mean(original_annotations)
    stdev_original_annotations = statistics.stdev(original_annotations)
    quantiles_original_annotations = statistics.quantiles(original_annotations, n=4)
    
    # write the stats to a json file
    data = {
        "noise_level": noise_level,
        "annotations_removed_per_class_this_run": annotations_removed_per_class_this_run,
        "areas_removed_this_run": {
            "mean": mean_area_removed_this_run,
            "stdev": stdev_area_removed_this_run,
            "quantiles": quantiles_area_removed_this_run
        },
        "original_annotations_this_run": {
            "mean": mean_original_annotations_this_run,
            "stdev": stdev_original_annotations_this_run,
            "quantiles": quantiles_original_annotations_this_run
        },
        "annotations_removed_per_class": annotations_removed_per_class,
        "areas_removed": {
            "mean": mean_area_removed,
            "stdev": stdev_area_removed,
            "quantiles": quantiles_area_removed
        },
        "original_annotations": {
            "mean": mean_original_annotations,
            "stdev": stdev_original_annotations,
            "quantiles": quantiles_original_annotations
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



def generate_stats_type1(labels_folder, images_folder, target_labels_folder, target_images_folder, seeds, file_name, num_of_classes=20):
    print(seeds)
    # Initialize the dictionary to store the annotations removed per file
    annotations_removed_dict = {}
    original_annotation_files = os.listdir(labels_folder)
    for annotation_file in original_annotation_files:
        annotations_removed_dict[annotation_file] = []
    # Initialize the array to store the number of annotations removed per class
    annotations_removed_per_class = [0] * num_of_classes
    # Initialize the array to store the areas of the removed annotations
    areas_removed = []
    # Initialize the array to store the number of original annotations
    original_annotations = []

    for noise_level in range(0, len(seeds)):
        seed = seeds[noise_level]
        print(f"Seed: {seed}")
        # generate the noise:
        generate_noise_type1(labels_folder, images_folder, target_labels_folder, target_images_folder, seed)
        # Initialize the DS to store the stats of this run
        annotations_removed_per_class_this_run = [0] * num_of_classes
        areas_removed_this_run = []
        original_annotations_this_run = []
        # get the corrupted label files
        corrupted_annotation_files = os.listdir(target_labels_folder)
        
        for file in corrupted_annotation_files:
            corrupted_lines = []
            if os.path.exists(os.path.join(labels_folder, file)):
                with open(os.path.join(labels_folder, file), "r") as f:
                    corrupted_lines = f.readlines()
            original_lines = []
            with open(os.path.join(target_labels_folder, file), "r") as f:
                original_lines = f.readlines()
            # get the annotations that were removed
            removed_lines = list(set(original_lines) - set(corrupted_lines))
            removed_lines_this_run = list(set(removed_lines) - set(annotations_removed_dict[file]))

            for line in removed_lines_this_run:
                class_id, x_center, y_center, bbox_width, bbox_height = line.split()
                annotations_removed_per_class_this_run[int(class_id)] += 1
                areas_removed_this_run.append(float(bbox_width) * float(bbox_height))
                original_annotations_this_run.append(len(original_lines))
            annotations_removed_dict[file].extend(removed_lines_this_run)
        
        # Calculate the statistics over the runs
        for i in range(num_of_classes):
            annotations_removed_per_class[i] += annotations_removed_per_class_this_run[i]
        areas_removed.extend(areas_removed_this_run)
        original_annotations.extend(original_annotations_this_run)

        # calculate and write the stats
        calculate_and_write_stats(file_name, noise_level, annotations_removed_per_class_this_run, areas_removed_this_run, original_annotations_this_run,
            annotations_removed_per_class, areas_removed, original_annotations, num_of_classes)

    # collect the labels and images
    collect_labels_and_images(labels_folder, images_folder, target_labels_folder, target_images_folder)

# seeds for the data split: 12, 22, 42
labels_folder = "./../data2/PASCAL/labels/train"
images_folder = "./../data2/PASCAL/images/train"
target_labels_folder = "./../data2/PASCAL/noise1/labels"
target_images_folder = "./../data2/PASCAL/noise1/images"

all_images_folder = "./../data2/PASCAL/AllImages"
all_labels_folder = "./../data2/PASCAL/AllLabels"

file_name = "./exp1_stats_run2.json"

seeds = [14, 15, 16, 17, 18]

# get the data split
original_images_folder = "./../../results/exp1/YOLO/new/exp1_run_2_5/Research/data/PASCAL/images/train"
original_target_images_folder = "./../../results/exp1/YOLO/new/exp1_run_2_5/Research/data/PASCAL/noise1/images"

# split.collect_labels_and_images_type1_noise(original_images_folder, original_target_images_folder, all_labels_folder, labels_folder, all_images_folder, images_folder)
print("Stats")
generate_stats_type1(labels_folder, images_folder, target_labels_folder, target_images_folder, seeds, file_name)