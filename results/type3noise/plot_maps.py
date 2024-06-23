import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

# Initialize lists to store mAP values for different models
yolo_maps = [[] for _ in range(3)]
brain_tumor_maps = []
vis_maps = []
faster_rcnn_maps = []

# Read the mAP values from the file
with open('./mAPs.txt', 'r') as f:
    lines = f.readlines()
    brain_tumor_maps = [float(x) for x in lines[1].split()[1:]]
    vis_maps = [float(x) for x in lines[2].split()[1:]]
    faster_rcnn_maps = [float(x) for x in lines[3].split()[1:]]

yolo_result_files = os.listdir("./YOLO")
yolo_result_files = [x for x in yolo_result_files if x.endswith('.txt')]

for (i, file) in enumerate(yolo_result_files):
    with open(f'./YOLO/{file}', 'r') as f:
        lines = f.readlines()
        for line in lines:
            yolo_maps[i].append(float(line.split()[3]))

# Function to calculate percentual difference from baseline
def calculate_percentual_difference(maps):
    baseline = maps[0]
    return [(x - baseline) / baseline * 100 for x in maps]

# Calculate percentual differences for YOLO runs
yolo_diffs = [calculate_percentual_difference(run) for run in yolo_maps]
yolo_diffs = np.array(yolo_diffs)

# Calculate mean and confidence intervals for YOLO
yolo_mean = np.mean(yolo_diffs, axis=0)
yolo_std = np.std(yolo_diffs, axis=0, ddof=1)
confidence_level = 0.95
degrees_freedom = yolo_diffs.shape[0] - 1

# Margin of error
yolo_margin_of_error = yolo_std / np.sqrt(yolo_diffs.shape[0]) * t.ppf((1 + confidence_level) / 2., degrees_freedom)

# Calculate percentual differences for other models
brain_tumor_diff = calculate_percentual_difference(brain_tumor_maps)
vis_diff = calculate_percentual_difference(vis_maps)
faster_rcnn_diff = calculate_percentual_difference(faster_rcnn_maps)

# Noise levels
noise_levels = list(range(6))  # [0, 1, 2, 3, 4, 5]

# Plotting
plt.figure(figsize=(10, 6))

# Plot YOLO with shaded confidence intervals
plt.plot(noise_levels, yolo_mean, label='YOLO with PASCAL', marker='o', color='blue')
plt.fill_between(noise_levels, yolo_mean - yolo_margin_of_error, yolo_mean + yolo_margin_of_error, color='blue', alpha=0.1)

# Plot other models
plt.plot(noise_levels, brain_tumor_diff, label='YOLO with Brain Tumor', marker='o', color='green')
plt.plot(noise_levels, vis_diff, label='YOLO with VisDrone', marker='o', color='red')
plt.plot(noise_levels, faster_rcnn_diff, label='Faster R-CNN with PASCAL', marker='o', color='purple')

plt.axhline(0, color='grey', linestyle='--', linewidth=0.7)  # Baseline line

plt.xlabel('Noise Level', fontsize=15)
plt.ylabel('Percentage Difference in mAP@50-95 \nfrom Baseline (%)', fontsize=15)
plt.title('Percentage decrease of mAP@50-95 compared to the baseline\n for increasing levels of inaccurate bounding boxes', fontsize=20)
plt.legend(fontsize=16)
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# set the min and max limits for the y-axis
plt.ylim(-50, 10)
plt.savefig('exp3.png')