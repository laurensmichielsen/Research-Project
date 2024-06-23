import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

stat_files = os.listdir('./')
stat_files = [file for file in stat_files if file.endswith('.json')]
data = []
for file in stat_files:
    with open(file, 'r') as f:
        data.append(json.load(f))

id_class_dict = {0 : "areoplane", 1: "bicycle", 2: "bird", 3: "boat", 4: "bottle",
        5: "bus", 6: "car", 7: "cat", 8: "chair", 9: "cow", 10: "dining table",
        11: "dog", 12: "horse", 13: "motorbike", 14: "person", 15: "potted plant", 16: "sheep",
        17: "sofa", 18: "train", 19: "tv/monitor"}

class_names = [id_class_dict[i] for i in range(len(id_class_dict))]

def plot_and_save_confusion_matrix(confusion_matrix, filename, title):
    plt.figure(figsize=(14, 12))
    ax = sns.heatmap(confusion_matrix, annot=True, fmt='.1f', cmap='Blues', 
                     xticklabels=class_names, yticklabels=class_names, annot_kws={"size": 10})
    plt.xlabel('True Labels')
    plt.ylabel('Corrupted Labels')
    plt.title(title)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()  # Adjust the layout to make room for the rotated labels
    plt.savefig(filename)
    plt.close()

for i in range(0, 5):
    data1 = data[0][i]
    data2 = data[1][i]
    data3 = data[2][i]

    confusion_matrix_this_run_1 = np.array(data1['confusion_matrix_this_run'])
    confusion_matrix_this_run_2 = np.array(data2['confusion_matrix_this_run'])
    confusion_matrix_this_run_3 = np.array(data3['confusion_matrix_this_run'])

    stacked_confusion_matrix_this_run = np.stack([confusion_matrix_this_run_1, confusion_matrix_this_run_2, confusion_matrix_this_run_3])
    confusion_matrix_this_run_avg = np.mean(stacked_confusion_matrix_this_run, axis=0)
    confusion_matrix_this_run_avg = np.round(confusion_matrix_this_run_avg, 1)

    confusion_matrix_1 = np.array(data1['confusion_matrix'])
    confusion_matrix_2 = np.array(data2['confusion_matrix'])
    confusion_matrix_3 = np.array(data3['confusion_matrix'])

    stacked_confusion_matrix = np.stack([confusion_matrix_1, confusion_matrix_2, confusion_matrix_3])
    confusion_matrix_avg = np.mean(stacked_confusion_matrix, axis=0)
    confusion_matrix_avg = np.round(confusion_matrix_avg, 1)

    plot_and_save_confusion_matrix(confusion_matrix_this_run_avg, f'confusion_matrix_this_run_avg_{i}.png', f'Confusion Matrix This Run Avg {i}')
    plot_and_save_confusion_matrix(confusion_matrix_avg, f'confusion_matrix_avg_{i}.png', f'Confusion Matrix Avg {i}')

