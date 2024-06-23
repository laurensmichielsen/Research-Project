import os
import matplotlib.pyplot as plt
import numpy as np
import json

id_class_dict = {
    0: "areoplane", 1: "bicycle", 2: "bird", 3: "boat", 4: "bottle",
    5: "bus", 6: "car", 7: "cat", 8: "chair", 9: "cow", 10: "dining table",
    11: "dog", 12: "horse", 13: "motorbike", 14: "person", 15: "potted plant", 16: "sheep",
    17: "sofa", 18: "train", 19: "tv/monitor"
}

def plot_percentual_difference_over_noise_levels(exp_nr):
    json_files = os.listdir(f"./exp{exp_nr}")
    json_files = [f for f in json_files if f.endswith(".json")]

    data = []
    for file in json_files:
        with open(os.path.join(f"./exp{exp_nr}", file), 'r') as f:
            data.append(json.load(f))

    num_classes = len(id_class_dict)
    num_noise_levels = len(data[0])  # assuming all experiments have the same number of noise levels

    # Initialize array to store average precision per class and noise level
    avg_precision_per_class = np.zeros((num_classes, num_noise_levels))

    for exp_data in data:
        for noise_level in range(num_noise_levels):
            aps = exp_data[noise_level]['aps']
            for class_idx in range(num_classes):
                avg_precision_per_class[class_idx, noise_level] += aps[class_idx]

    avg_precision_per_class /= len(data)  # average over the number of experiments

    # Calculate percentual difference relative to noise level 0
    percentual_difference = np.zeros_like(avg_precision_per_class)

    for class_idx in range(num_classes):
        percentual_difference[class_idx] = (avg_precision_per_class[class_idx] / avg_precision_per_class[class_idx, 0] - 1) * 100

    # Plotting
    plt.figure(figsize=(13, 8))

    # Use a qualitative colormap for distinct colors
    colors = plt.get_cmap('tab20').colors

    for class_idx in range(num_classes):
        class_name = id_class_dict[class_idx]
        plt.plot(range(num_noise_levels), percentual_difference[class_idx], label=class_name, color=colors[class_idx])

    plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)  # horizontal line at percentual difference 0
    plt.xlabel('Noise Levels', fontsize=15)
    plt.ylabel('Percentage Difference (%)', fontsize=15)
    plt.title(f'Percentage Difference of AP@50-95 over Noise Levels compared\nto the baseline for increasing levels of wrong classification labels', fontsize=22)
    plt.xticks(range(num_noise_levels), [f'Noise {i}' for i in range(num_noise_levels)])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.ylim(-65, 5)
    plt.savefig(f"./exp{exp_nr}/percentual_difference.png")

# Example usage:
plot_percentual_difference_over_noise_levels(4)

# import os
# import matplotlib.pyplot as plt
# import numpy as np
# import json

# id_class_dict = {
#     0: "areoplane", 1: "bicycle", 2: "bird", 3: "boat", 4: "bottle",
#     5: "bus", 6: "car", 7: "cat", 8: "chair", 9: "cow", 10: "dining table",
#     11: "dog", 12: "horse", 13: "motorbike", 14: "person", 15: "potted plant", 16: "sheep",
#     17: "sofa", 18: "train", 19: "tv/monitor"
# }

# def plot_percentual_difference_over_noise_levels(exp_nr):
#     json_files = os.listdir(f"./exp{exp_nr}")
#     json_files = [f for f in json_files if f.endswith(".json")]

#     data = []
#     for file in json_files:
#         with open(os.path.join(f"./exp{exp_nr}", file), 'r') as f:
#             data.append(json.load(f))

#     num_classes = len(id_class_dict)
#     num_noise_levels = len(data[0])  # assuming all experiments have the same number of noise levels

#     # Initialize array to store average precision per class and noise level
#     avg_precision_per_class = np.zeros((num_classes, num_noise_levels))

#     for exp_data in data:
#         for noise_level in range(num_noise_levels):
#             aps = exp_data[noise_level]['aps']
#             for class_idx in range(num_classes):
#                 avg_precision_per_class[class_idx, noise_level] += aps[class_idx]

#     avg_precision_per_class /= len(data)  # average over the number of experiments

#     # Calculate percentual difference relative to noise level 0
#     percentual_difference = np.zeros_like(avg_precision_per_class)

#     for class_idx in range(num_classes):
#         percentual_difference[class_idx] = (avg_precision_per_class[class_idx] / avg_precision_per_class[class_idx, 0] - 1) * 100

#     # Plotting
#     plt.figure(figsize=(12, 8))

#     for class_idx in range(num_classes):
#         class_name = id_class_dict[class_idx]
#         plt.plot(range(num_noise_levels), percentual_difference[class_idx], label=class_name)

#     plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)  # horizontal line at percentual difference 0
#     plt.xlabel('Noise Levels')
#     plt.ylabel('Percentual Difference (%)')
#     plt.title(f'Percentual Difference of Average Precision per Class over Noise Levels (Benchmark: Noise Level 0, Experiment {exp_nr})')
#     plt.xticks(range(num_noise_levels), [f'Noise {i}' for i in range(num_noise_levels)])
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(f"./exp{exp_nr}/percentual_difference.png")

# # Example usage:
# plot_percentual_difference_over_noise_levels(4)

# import os
# import matplotlib.pyplot as plt
# import numpy as np
# import json

# id_class_dict = {
#     0: "areoplane", 1: "bicycle", 2: "bird", 3: "boat", 4: "bottle",
#     5: "bus", 6: "car", 7: "cat", 8: "chair", 9: "cow", 10: "dining table",
#     11: "dog", 12: "horse", 13: "motorbike", 14: "person", 15: "potted plant", 16: "sheep",
#     17: "sofa", 18: "train", 19: "tv/monitor"
# }

# def plot_class_over_noise_levels_per_experiment(exp_nr):
#     json_files = os.listdir(f"./exp{exp_nr}")
#     json_files = [f for f in json_files if f.endswith(".json")]

#     data = []
#     for file in json_files:
#         with open(os.path.join(f"./exp{exp_nr}", file), 'r') as f:
#             data.append(json.load(f))

#     num_classes = len(id_class_dict)
#     num_noise_levels = len(data[0])  # assuming all experiments have the same number of noise levels

#     # Initialize array to store average precision per class and noise level
#     avg_precision_per_class = np.zeros((num_classes, num_noise_levels))

#     for exp_data in data:
#         for noise_level in range(num_noise_levels):
#             aps = exp_data[noise_level]['aps']
#             for class_idx in range(num_classes):
#                 avg_precision_per_class[class_idx, noise_level] += aps[class_idx]

#     avg_precision_per_class /= len(data)  # average over the number of experiments

#     # Plotting
#     plt.figure(figsize=(12, 8))

#     for class_idx in range(num_classes):
#         class_name = id_class_dict[class_idx]
#         plt.plot(range(num_noise_levels), avg_precision_per_class[class_idx], label=class_name)

#     plt.xlabel('Noise Levels')
#     plt.ylabel('Average Precision')
#     plt.title(f'Average Precision per Class over Noise Levels (Experiment {exp_nr})')
#     plt.xticks(range(num_noise_levels), [f'Noise {i}' for i in range(num_noise_levels)])
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(f"./exp{exp_nr}/ap_per_class.png")

# # Example usage:
# plot_class_over_noise_levels_per_experiment(1)
