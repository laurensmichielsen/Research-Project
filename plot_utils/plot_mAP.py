import os
import numpy as np
import matplotlib.pyplot as plt


def plot_mp_mr(results_dir, filename):
    # get the results from the txt files
    result_files = os.listdir(results_dir)
    for file in result_files:
        if not file.endswith(".txt"):
            result_files.remove(file)
    # create a dictionary to store the results: map 0, 1, 2, 3, 4, 5 to empty lists
    results_dict_mAP = {i: [] for i in range(6)}
    # iterate over the files
    for file in result_files:
        with open(os.path.join(results_dir, file), 'r') as f:
            print(file)
            lines = f.readlines()
            for line in lines:
                line = line.split()
                noise_level = int(line[0])
                mAP = float(line[3])
                results_dict_mAP[noise_level].append(mAP)
    # for each noise level compute the 95% confidence interval and plot the results with the noise levels on the x-axis and the mean precision and recall on the y-axis
    # plot the mean as a thick line and lightly colour the area between the confidence intervals
    # map 0, 1, 2, 3, 4, 5 to the corresponding noise levels which is the noise level times 10%
    
    mAP_means = [np.mean(results_dict_mAP[i]) for i in range(6)]
    mAP_std = [np.std(results_dict_mAP[i]) for i in range(6)]

    noise_levels = [i for i in range(6)]
    
    sample_size = np.sqrt(3)
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, mAP_means, label='mAP@50-95', marker='o', color='blue')
    plt.fill_between(noise_levels, np.array(mAP_means) - (1.96 / sample_size) * np.array(mAP_std), np.array(mAP_means) + (1.96 / sample_size) * np.array(mAP_std), alpha=0.1)

    plt.xlabel('Noise level', fontsize=14)
    plt.ylabel('mean Average Precision', fontsize=14)
    plt.title('mAP@50-95 of YOLO trained on PASCAL with increasing\nlevels of missing annotations', fontsize=20)
    plt.ylim(0.44, 0.575)
    plt.grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=16)
    plt.savefig(os.path.join(results_dir, "plots", filename))
    

plot_mp_mr('./../results/type1noise/YOLO', 'mAP_exp1.png') 