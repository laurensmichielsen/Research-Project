import os
import numpy as np
import matplotlib.pyplot as plt

def plot_mAP_at_50(results_dir, filename):
    result_files = os.listdir(results_dir)
    # remove all the elements in result_files that are directories
    for file in result_files:
        if not file.endswith(".txt"):
            result_files.remove(file)
    results_dict_mAP50 = {i: [] for i in range(6)}
    

    for file in result_files:
        with open(os.path.join(results_dir, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                noise_level = int(line[0])
                mAP50 = float(line[4])
                
                results_dict_mAP50[noise_level].append(mAP50)
                
    mAP50_means = [np.mean(results_dict_mAP50[i]) for i in range(6)]
    mAP50_std = [np.std(results_dict_mAP50[i]) for i in range(6)]
    noise_levels = [i for i in range(6)]
    sample_size = np.sqrt(3)
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, mAP50_means, label='mAP@50', marker='o', color='blue')
    plt.fill_between(noise_levels, np.array(mAP50_means) - (1.96 / sample_size) * np.array(mAP50_std), np.array(mAP50_means) + (1.96 / sample_size) * np.array(mAP50_std), alpha=0.1)
    
    plt.xlabel('Noise level', fontsize=14)
    plt.ylabel('mAP@50', fontsize=14)
    plt.title('mAP@50 of YOLO trained on PASCAL with increasing\nlevels of wrong classification labels', fontsize=20)
    plt.legend(fontsize=16)
    plt.grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(0.60, 0.75)
    plt.savefig(os.path.join(results_dir, "plots", filename))

plot_mAP_at_50(results_dir="./../results/type4noise/YOLO", filename="mAP@50_exp4.png")

