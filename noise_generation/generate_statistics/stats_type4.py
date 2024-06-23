import generate_noise_type4 as g
import os
import statistics
import collect_data_split as split
import json 

def write_to_file(file_name, confusion_matrix_this_run, confusion_matrix, noise_level):
    number_of_switches_this_run_per_class = [0 for i in range(0, len(confusion_matrix_this_run))]
    number_of_switches_per_class = [0 for i in range(0, len(confusion_matrix))]
    number_of_switches_to_this_run_per_class = [0 for i in range(0, len(confusion_matrix_this_run))]
    number_of_switches_to_per_class = [0 for i in range(0, len(confusion_matrix))]
    total_switches_this_run = 0
    total_switches = 0
    for i in range(0, len(confusion_matrix_this_run)):
        for j in range(0, len(confusion_matrix_this_run[i])):
            number_of_switches_this_run_per_class[i] += confusion_matrix_this_run[i][j]
            number_of_switches_to_this_run_per_class[j] += confusion_matrix_this_run[i][j]
            total_switches_this_run += confusion_matrix_this_run[i][j]
            number_of_switches_per_class[i] += confusion_matrix[i][j]
            number_of_switches_to_per_class[j] += confusion_matrix[i][j]
            total_switches += confusion_matrix[i][j]
    with open(file_name, 'a') as f:
        print(noise_level)
        f.write(f'{noise_level}\n')
        for i in range(0, len(confusion_matrix_this_run)):
            for j in range(0, len(confusion_matrix_this_run[i])):
                f.write(f'{confusion_matrix_this_run[i][j]} ')
            f.write('\n')
        f.write('\n')
        for i in range(0, len(confusion_matrix_this_run)):
            f.write(f'{number_of_switches_this_run_per_class[i]} ')
        f.write('\n')
        for i in range(0, len(number_of_switches_to_this_run_per_class)):
            f.write(f'{number_of_switches_to_this_run_per_class[i]} ')
        f.write('\n')
        f.write(f'{total_switches_this_run}\n')
        for i in range(0, len(confusion_matrix)):
            for j in range(0, len(confusion_matrix[i])):
                f.write(f'{confusion_matrix[i][j]} ')
            f.write('\n')
        f.write('\n')
        for i in range(0, len(confusion_matrix)):
            f.write(f'{number_of_switches_per_class[i]} ')
        f.write('\n')
        for i in range(0, len(number_of_switches_to_per_class)):
            f.write(f'{number_of_switches_to_per_class[i]} ')
        f.write('\n')
        f.write(f'{total_switches}\n')
        f.write('\n')

def write_stats_to_file_json(file_name, confusion_matrix_this_run, confusion_matrix, noise_level):
    number_of_switches_this_run_per_class = [0 for i in range(0, len(confusion_matrix_this_run))]
    number_of_switches_per_class = [0 for i in range(0, len(confusion_matrix))]
    number_of_switches_to_this_run_per_class = [0 for i in range(0, len(confusion_matrix_this_run))]
    number_of_switches_to_per_class = [0 for i in range(0, len(confusion_matrix))]
    total_switches_this_run = 0
    total_switches = 0
    for i in range(0, len(confusion_matrix_this_run)):
        for j in range(0, len(confusion_matrix_this_run[i])):
            number_of_switches_this_run_per_class[i] += confusion_matrix_this_run[i][j]
            number_of_switches_to_this_run_per_class[j] += confusion_matrix_this_run[i][j]
            total_switches_this_run += confusion_matrix_this_run[i][j]
            number_of_switches_per_class[i] += confusion_matrix[i][j]
            number_of_switches_to_per_class[j] += confusion_matrix[i][j]
            total_switches += confusion_matrix[i][j]
    # Prepare data to be written to JSON
    data = {
        "noise_level": noise_level,
        "confusion_matrix_this_run": confusion_matrix_this_run,
        "confusion_matrix": confusion_matrix,
        "number_of_switches_per_class": number_of_switches_per_class,
        "number_of_switches_to_per_class": number_of_switches_to_per_class,
        "total_switches": total_switches,
        "number_of_switches_this_run_per_class": number_of_switches_this_run_per_class,
        "number_of_switches_to_this_run_per_class": number_of_switches_to_this_run_per_class,
        "total_switches_this_run": total_switches_this_run,
    }

    # Open the JSON file in read mode
    try:
        with open(file_name, 'r') as json_file:
            # Load existing data from the JSON file
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty list
        existing_data = []

    # Append new data to the existing list
    existing_data.append(data)

    # Open the JSON file in write mode
    with open(file_name, 'w') as json_file:
        # Write the updated list of data objects to the JSON file
        json.dump(existing_data, json_file, indent=4)

        

def generate_stats_type_4(label_folder, target_label_folder, seeds, file_name, num_classes=20):
    g.collect_labels_and_images(label_folder, target_label_folder)
    # initialize the dictionary to store the noise
    label_files = os.listdir(label_folder)
    noise_dict = {}
    for file in label_files:
        noise_dict[file] = []
    # Initialize the confusion matrix
    confusion_matrix = [[0 for i in range(num_classes)] for j in range(num_classes)]
    # Generate the stats
    for noise_level in range(0, len(seeds)):
        # generate the noise
        g.generate_noise_type4(label_folder, target_label_folder, seeds[noise_level])
        # Get the label files that have corrupted annotations
        corrupted_label_files = os.listdir(target_label_folder)
        # Initialize the confusion matrix for this run
        confusion_matrix_this_run = [[0 for i in range(num_classes)] for j in range(num_classes)]
        # iterate over the corrupted label files 
        for file in corrupted_label_files:
            # read the corrupted file
            all_corrupted_lines = []
            with open(os.path.join(target_label_folder, file), 'r') as f:
                all_corrupted_lines = f.readlines()
            # read the original file
            original_lines = []
            with open(os.path.join(label_folder, file), 'r') as f:
                original_lines = f.readlines()
            # Get the lines that were corrupted
            corrupted_lines = list(set(all_corrupted_lines) - set(original_lines))
            # get the lines that were corrupted in this run
            corrupted_lines_this_run = list(set(corrupted_lines) - set(noise_dict[file]))
            if len(corrupted_lines_this_run) > 0:
                for line in corrupted_lines_this_run:
                    class_id, _, _, _, _ = line.split()
                    class_id = int(class_id)
                    original_class_id, _, _, _, _ = original_lines[all_corrupted_lines.index(line)].split()
                    original_class_id = int(original_class_id)
                    # update the confusion matrix
                    confusion_matrix_this_run[original_class_id][class_id] += 1
            # update the noise dictionary
            noise_dict[file] = corrupted_lines
        # update the confusion matrix
        for i in range(0, num_classes):
            for j in range(0, num_classes):
                confusion_matrix[i][j] += confusion_matrix_this_run[i][j]
        # write the confusion matrices to the file
        write_stats_to_file_json(file_name, confusion_matrix_this_run, confusion_matrix, noise_level)
    # collect the noise
    g.collect_labels_and_images(label_folder, target_label_folder)


label_folder = "./../data2/PASCAL/labels/train"
target_label_folder = "./../data2/PASCAL/noise4"
seeds = [2, 3, 4, 5, 6]
file_name = "./exp4_stats_run0.json"

all_labels_folder = "./../data2/PASCAL/AllLabels"
original_labels_folder = "./../../results/exp4/YOLO/exp4_run_0_5/Research/data/PASCAL/labels/train"
original_target_labels_folder = "./../../results/exp4/YOLO/exp4_run_0_5/Research/data/PASCAL/noise4"

split.collect_labels_and_images_type2_3_4_noise(original_labels_folder, original_target_labels_folder, all_labels_folder, label_folder)
print("stats")
generate_stats_type_4(label_folder, target_label_folder, seeds, file_name)

