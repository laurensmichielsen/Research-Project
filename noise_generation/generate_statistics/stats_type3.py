import os
from generate_noise_type3 import generate_noise_type3, collect_labels_and_images
import statistics
import collect_data_split as split
import json


def write_stats_to_file_json(file_name, noise_level, number_of_corrupted_annotations_per_class_this_run, mean_IoU_this_run,
        stdev_IoU_this_run, quantiles_IoU_this_run, mean_area_this_run, stdev_area_this_run, quantiles_area_this_run,
        number_of_corrupted_annotations_per_class_so_far, mean_IoU_so_far, stdev_IoU_so_far, quantiles_IoU_so_far,
        mean_area_so_far, stdev_area_so_far, quantiles_area_so_far):
    # Prepare data to be written to JSON
    data = {
        "noise_level": noise_level,
        "number_of_corrupted_annotations_per_class_this_run": number_of_corrupted_annotations_per_class_this_run,
        "IoU_this_run": {
            "mean": mean_IoU_this_run,
            "stdev": stdev_IoU_this_run,
            "quantiles": quantiles_IoU_this_run
        },
        "areas_this_run": {
            "mean": mean_area_this_run,
            "stdev": stdev_area_this_run,
            "quantiles": quantiles_area_this_run
        },
        "number_of_corrupted_annotations_per_class_so_far": number_of_corrupted_annotations_per_class_so_far,
        "IoU_so_far": {
            "mean": mean_IoU_so_far,
            "stdev": stdev_IoU_so_far,
            "quantiles": quantiles_IoU_so_far
        },
        "areas_so_far": {
            "mean": mean_area_so_far,
            "stdev": stdev_area_so_far,
            "quantiles": quantiles_area_so_far
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

def calc_iou(o_x, o_y, o_w, o_h, c_x, c_y, c_w, c_h):
    o_x1 = o_x - o_w / 2
    o_y1 = o_y - o_h / 2
    o_x2 = o_x + o_w / 2
    o_y2 = o_y + o_h / 2
    c_x1 = c_x - c_w / 2
    c_y1 = c_y - c_h / 2
    c_x2 = c_x + c_w / 2
    c_y2 = c_y + c_h / 2
    x1 = max(o_x1, c_x1)
    y1 = max(o_y1, c_y1)
    x2 = min(o_x2, c_x2)
    y2 = min(o_y2, c_y2)
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    union = o_w * o_h + c_w * c_h - intersection
    if union == 0:
        return 0
    return intersection / union

def read_line(line):
    line = line.strip().split()
    class_id = int(line[0])
    x_center = float(line[1])
    y_center = float(line[2])
    width = float(line[3])
    height = float(line[4])
    return class_id, x_center, y_center, width, height

def generate_stats_type3(label_folder, target_label_folder, seeds, file_name, txt_file, num_classes=20):
    # Initialize the dictionary to store the corrupted annotations
    label_files = os.listdir(label_folder)
    corrupted_annotations_dict = {}
    for file in label_files:
        corrupted_annotations_dict[file] = []
    # Initialize the array to store the number of corrupted annotations per class
    number_of_corrupted_annotations_per_class = [0 for i in range(num_classes)]
    # Initialize the array to store the areas of the corrupted annotations
    areas_of_corrupted_annotations = []
    # Initialize the array to store the IoUs of the corrupted annotations
    IoUs_of_corrupted_annotations = []

    for noise_level in range(0, len(seeds)):
        print(f'Noise level: {noise_level}')
        # generate the noise
        generate_noise_type3(label_folder, target_label_folder, seeds[noise_level])
        # get the label files that have corrupted annotations
        corrupted_label_files = os.listdir(target_label_folder)
        # Initialize the dictionary to store the number of corrupted annotations per class
        number_of_corrupted_annotations_per_class_this_run = [0 for i in range(num_classes)]
        # Initialize the array to store the areas of the corrupted annotations this run
        areas_of_corrupted_annotations_this_run = []
        # Initialize the array to store the IoUs of the corrupted annotations this run
        IoUs_of_corrupted_annotations_this_run = []
        for file in corrupted_label_files:
            all_corrupted_lines = []
            with open(os.path.join(label_folder, file), 'r') as f:
                all_corrupted_lines = f.readlines()
            original_lines = []
            with open(os.path.join(target_label_folder, file), 'r') as f:
                original_lines = f.readlines()
            # Get the lines that were corrupted
            corrupted_lines = list(set(all_corrupted_lines) - set(original_lines))
            # get the lines that were corrupted in this run
            corrupted_lines_this_run = list(set(corrupted_lines) - set(corrupted_annotations_dict[file]))

            for line in corrupted_lines_this_run:
                # read the corrupted line
                corrupted_id, corrupted_x_center, corrupted_y_center, corrupted_width, corrupted_height = read_line(line)
                # read the original line
                idx = all_corrupted_lines.index(line)
                original_id, original_x_center, original_y_center, original_width, original_height = read_line(original_lines[idx])
                # update the number of corrupted annotations per class
                assert original_id == corrupted_id
                number_of_corrupted_annotations_per_class_this_run[original_id] += 1
                # update the areas of the corrupted annotations
                areas_of_corrupted_annotations_this_run.append(original_width * original_height)
                # update the IoUs of the corrupted annotations
                IoUs_of_corrupted_annotations_this_run.append(calc_iou(original_x_center, original_y_center, original_width, original_height, corrupted_x_center, corrupted_y_center, corrupted_width, corrupted_height))

            # update the dictionary
            corrupted_annotations_dict[file] = corrupted_lines
        # calculate the stats for this run
        # calculate the median, stdev, quantiles of the IoUs of this run
        mean_IoU = statistics.mean(IoUs_of_corrupted_annotations_this_run)
        stdev_IoU = statistics.stdev(IoUs_of_corrupted_annotations_this_run)
        quantiles_IoU = statistics.quantiles(IoUs_of_corrupted_annotations_this_run, n=4)
        # calculate the median, stdev, quantiles of the areas of this run
        mean_area = statistics.mean(areas_of_corrupted_annotations_this_run)
        stdev_area = statistics.stdev(areas_of_corrupted_annotations_this_run)
        quantiles_area = statistics.quantiles(areas_of_corrupted_annotations_this_run, n=4)

        # calculate the stats for the runs so far
        # update the number of corrupted annotations per class
        for i in range(0, len(number_of_corrupted_annotations_per_class)):
            number_of_corrupted_annotations_per_class[i] += number_of_corrupted_annotations_per_class_this_run[i]
        # update the areas of the corrupted annotations
        areas_of_corrupted_annotations.extend(areas_of_corrupted_annotations_this_run)
        # update the IoUs of the corrupted annotations
        IoUs_of_corrupted_annotations.extend(IoUs_of_corrupted_annotations_this_run)
        # calculate the median, stdev, quantiles of the IoUs of the runs so far
        mean_IoU_so_far = statistics.mean(IoUs_of_corrupted_annotations)
        stdev_IoU_so_far = statistics.stdev(IoUs_of_corrupted_annotations)
        quantiles_IoU_so_far = statistics.quantiles(IoUs_of_corrupted_annotations, n=4)
        # calculate the median, stdev, quantiles of the areas of the runs so far
        mean_area_so_far = statistics.mean(areas_of_corrupted_annotations)
        stdev_area_so_far = statistics.stdev(areas_of_corrupted_annotations)
        quantiles_area_so_far = statistics.quantiles(areas_of_corrupted_annotations, n=4)
        # write the stats to the file
        write_stats_to_file_json(file_name, noise_level, number_of_corrupted_annotations_per_class_this_run, mean_IoU, stdev_IoU, quantiles_IoU, mean_area, stdev_area, quantiles_area, number_of_corrupted_annotations_per_class, mean_IoU_so_far, stdev_IoU_so_far, quantiles_IoU_so_far, mean_area_so_far, stdev_area_so_far, quantiles_area_so_far)
    collect_labels_and_images(label_folder, target_label_folder)

label_folder = "./../data2/PASCAL/labels/train"
target_label_folder = "./../data2/PASCAL/noise3"
seeds = [8]
file_name = "./exp3_stats_run0.json"

all_labels_folder = "./../data2/PASCAL/AllLabels"
original_labels_folder = "./../../results/exp3/YOLO/exp3_run_0_5/Research/data/PASCAL/labels/train"
original_target_labels_folder = "./../../results/exp3/YOLO/exp3_run_0_5/Research/data/PASCAL/noise3"



# collect_labels_and_images(label_folder, target_label_folder)

# split.collect_labels_and_images_type2_3_4_noise(original_labels_folder, original_target_labels_folder, all_labels_folder, label_folder)
print("stats")
generate_stats_type3(label_folder, target_label_folder, seeds, file_name, "./exp3_stats_run0.txt")