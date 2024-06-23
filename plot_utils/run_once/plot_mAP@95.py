import os
import numpy as np
import matplotlib.pyplot as plt

def plot_mAP_at_95(results_dir, filename):
    result_files = os.listdir(results_dir)
    # remove all the elements in result_files that are directories
    for file in result_files:
        if not file.endswith(".txt"):
            result_files.remove(file)
    results_dict_mAP95 = {i: [] for i in range(6)}
    for file in result_files:
        with open(os.path.join(results_dir, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                noise_level = int(line[0])
                mAP95 = float(line[13])
                results_dict_mAP95[noise_level].append(mAP95)
    mAP95_means = [np.mean(results_dict_mAP95[i]) for i in range(6)]
    mAP95_std = [np.std(results_dict_mAP95[i]) for i in range(6)]
    noise_levels = [i*10 for i in range(6)]
    sample_size = np.sqrt(3)
    plt.plot(noise_levels, mAP95_means, label='mAP95')
    # plt.fill_between(noise_levels, np.array(mAP95_means) - (1.96 / sample_size) * np.array(mAP95_std), np.array(mAP95_means) + (1.96 / sample_size) * np.array(mAP95_std), alpha=0.2)
    plt.xlabel('Noise level in %')
    plt.ylabel('mAP@95')
    plt.legend()
    plt.savefig(os.path.join(results_dir, "plots", filename))

plot_mAP_at_95(results_dir="./../../results/type4noise/brain_tumor", filename="mAP@95_exp4_BT.png")
