import os
import numpy as np
import matplotlib.pyplot as plt

def plot_mAP_at_75(results_dir, filename):
    result_files = os.listdir(results_dir)
    # remove all the elements in result_files that are directories
    for file in result_files:
        if not file.endswith(".txt"):
            result_files.remove(file)
    results_dict_mAP75 = {i: [] for i in range(6)}
    print(result_files)
    for file in result_files:
        with open(os.path.join(results_dir, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                noise_level = int(line[0])
                mAP75 = float(line[9])
                results_dict_mAP75[noise_level].append(mAP75)
    mAP75_means = [np.mean(results_dict_mAP75[i]) for i in range(6)]
    mAP75_std = [np.std(results_dict_mAP75[i]) for i in range(6)]
    noise_levels = [i for i in range(6)]
    sample_size = np.sqrt(3)
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, mAP75_means, label='mAP@75', marker='o', color='blue')
    plt.fill_between(noise_levels, np.array(mAP75_means) - (1.96 / sample_size) * np.array(mAP75_std), np.array(mAP75_means) + (1.96 / sample_size) * np.array(mAP75_std), alpha=0.1)
    plt.xlabel('Noise level', fontsize=14)
    plt.ylabel('mAP@75', fontsize=14)
    plt.legend(fontsize=16)
    plt.grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(0.48, 0.64)
    plt.title('mAP@75 of YOLO trained on PASCAL with increasing\nlevels of missing annotations', fontsize=20)
    plt.savefig(os.path.join(results_dir, "plots", filename))

plot_mAP_at_75(results_dir="./../results/type1noise/YOLO", filename="mAP@75_exp1.png")
