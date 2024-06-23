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
    results_dict_mp = {i: [] for i in range(6)}
    results_dict_mr = {i: [] for i in range(6)}
    # iterate over the files
    for file in result_files:
        with open(os.path.join(results_dir, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                noise_level = int(line[0])
                mp = float(line[1])
                mr = float(line[2])
                results_dict_mp[noise_level].append(mp)
                results_dict_mr[noise_level].append(mr)
    # for each noise level compute the 95% confidence interval and plot the results with the noise levels on the x-axis and the mean precision and recall on the y-axis
    # plot the mean as a thick line and lightly colour the area between the confidence intervals
    # map 0, 1, 2, 3, 4, 5 to the corresponding noise levels which is the noise level times 10%
    
    mp_means = [np.mean(results_dict_mp[i]) for i in range(6)]
    mp_std = [np.std(results_dict_mp[i]) for i in range(6)]
    mr_means = [np.mean(results_dict_mr[i]) for i in range(6)]
    mr_std = [np.std(results_dict_mr[i]) for i in range(6)]
    noise_levels = [i*10 for i in range(6)]
    sample_size = np.sqrt(3)
    plt.plot(noise_levels, mp_means, label='Mean Precision')
    plt.fill_between(noise_levels, np.array(mp_means) - (1.96 / sample_size) * np.array(mp_std), np.array(mp_means) + (1.96 / sample_size) * np.array(mp_std), alpha=0.2)
    plt.plot(noise_levels, mr_means, label='Mean Recall')
    plt.fill_between(noise_levels, np.array(mr_means) - (1.96 / sample_size) *  np.array(mr_std), np.array(mr_means) + (1.96 / sample_size) * np.array(mr_std), alpha=0.2)
    plt.xlabel('Noise level in %')
    plt.ylabel('Mean Precision and Recall')
    plt.legend()
    plt.savefig(os.path.join(results_dir, "plots", filename))
    

plot_mp_mr(results_dir="./../results/type4noise/YOLO", filename="mp_mr_exp4_yolo.png")