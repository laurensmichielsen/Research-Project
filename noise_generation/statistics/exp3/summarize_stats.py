import os
import json
import numpy as np

stat_files = os.listdir('./')
stat_files = [file for file in stat_files if file.endswith('.json')]

data = []

for file in stat_files:
    with open(file, 'r') as f:
        data.append(json.load(f))

for i in range(0, 5):
    data1 = data[0][i]
    data2 = data[1][i]
    data3 = data[2][i]

    number_of_corrupted_annotations_per_class_this_run_avg = np.mean([
        data1['number_of_corrupted_annotations_per_class_this_run'],
        data2['number_of_corrupted_annotations_per_class_this_run'],
        data3['number_of_corrupted_annotations_per_class_this_run']
    ], axis=0).tolist()

    IoU_this_run_mean_avg = np.mean([
        data1['IoU_this_run']['mean'],
        data2['IoU_this_run']['mean'],
        data3['IoU_this_run']['mean']
    ])

    IoU_this_run_stdev_avg = np.mean([
        data1['IoU_this_run']['stdev'],
        data2['IoU_this_run']['stdev'],
        data3['IoU_this_run']['stdev']
    ])

    IoU_this_run_quantiles_avg = np.mean([
        data1['IoU_this_run']['quantiles'],
        data2['IoU_this_run']['quantiles'],
        data3['IoU_this_run']['quantiles']
    ], axis=0).tolist()

    areas_this_run_mean_avg = np.mean([
        data1['areas_this_run']['mean'],
        data2['areas_this_run']['mean'],
        data3['areas_this_run']['mean']
    ])

    areas_this_run_stdev_avg = np.mean([
        data1['areas_this_run']['stdev'],
        data2['areas_this_run']['stdev'],
        data3['areas_this_run']['stdev']
    ])

    areas_this_run_quantiles_avg = np.mean([
        data1['areas_this_run']['quantiles'],
        data2['areas_this_run']['quantiles'],
        data3['areas_this_run']['quantiles']
    ], axis=0).tolist()

    number_of_corrupted_annotations_per_class_so_far_avg = np.mean([
        data1['number_of_corrupted_annotations_per_class_so_far'],
        data2['number_of_corrupted_annotations_per_class_so_far'],
        data3['number_of_corrupted_annotations_per_class_so_far']
    ], axis=0).tolist()

    IoU_so_far_mean_avg = np.mean([
        data1['IoU_so_far']['mean'],
        data2['IoU_so_far']['mean'],
        data3['IoU_so_far']['mean']
    ])

    IoU_so_far_stdev_avg = np.mean([
        data1['IoU_so_far']['stdev'],
        data2['IoU_so_far']['stdev'],
        data3['IoU_so_far']['stdev']
    ])

    IoU_so_far_quantiles_avg = np.mean([
        data1['IoU_so_far']['quantiles'],
        data2['IoU_so_far']['quantiles'],
        data3['IoU_so_far']['quantiles']
    ], axis=0).tolist()

    areas_so_far_mean_avg = np.mean([
        data1['areas_so_far']['mean'],
        data2['areas_so_far']['mean'],
        data3['areas_so_far']['mean']
    ])

    areas_so_far_stdev_avg = np.mean([
        data1['areas_so_far']['stdev'],
        data2['areas_so_far']['stdev'],
        data3['areas_so_far']['stdev']
    ])

    areas_so_far_quantiles_avg = np.mean([
        data1['areas_so_far']['quantiles'],
        data2['areas_so_far']['quantiles'],
        data3['areas_so_far']['quantiles']
    ], axis=0).tolist()

    # write to file

    os.makedirs('./results/type3noise', exist_ok=True)
    with open(os.path.join('./results/type3noise', f'average_stats{i}.txt'), 'w') as f:
        f.write(f'number_of_corrupted_annotations_per_class_this_run_avg: {number_of_corrupted_annotations_per_class_this_run_avg}\n')
        f.write(f'IoU_this_run_mean_avg: {IoU_this_run_mean_avg}\n')
        f.write(f'IoU_this_run_stdev_avg: {IoU_this_run_stdev_avg}\n')
        f.write(f'IoU_this_run_quantiles_avg: {IoU_this_run_quantiles_avg}\n')
        f.write(f'areas_this_run_mean_avg: {areas_this_run_mean_avg}\n')
        f.write(f'areas_this_run_stdev_avg: {areas_this_run_stdev_avg}\n')
        f.write(f'areas_this_run_quantiles_avg: {areas_this_run_quantiles_avg}\n')
        f.write(f'number_of_corrupted_annotations_per_class_so_far_avg: {number_of_corrupted_annotations_per_class_so_far_avg}\n')
        f.write(f'IoU_so_far_mean_avg: {IoU_so_far_mean_avg}\n')
        f.write(f'IoU_so_far_stdev_avg: {IoU_so_far_stdev_avg}\n')
        f.write(f'IoU_so_far_quantiles_avg: {IoU_so_far_quantiles_avg}\n')
        f.write(f'areas_so_far_mean_avg: {areas_so_far_mean_avg}\n')
        f.write(f'areas_so_far_stdev_avg: {areas_so_far_stdev_avg}\n')
        f.write(f'areas_so_far_quantiles_avg: {areas_so_far_quantiles_avg}\n')