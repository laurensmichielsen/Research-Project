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
    plt.plot(noise_levels, mAP_means, label='mAP')

    plt.xlabel('Noise level')
    plt.ylabel('mean Average Precision')
    # plt.ylim(0.45, 0.575)
    plt.legend()
    plt.savefig(os.path.join(results_dir, "plots", filename))
    

plot_mp_mr('./../../results/type4noise/brain_tumor', 'mAP_exp4_BT.png') 