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

    annotations_per_class_this_run_avg = np.mean([
        data1['annotations_per_class_this_run'],
        data2['annotations_per_class_this_run'],
        data3['annotations_per_class_this_run']
    ], axis=0).tolist()

    annotations_per_class_avg = np.mean([
        data1['annotations_per_class'],
        data2['annotations_per_class'],
        data3['annotations_per_class']
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

    highest_IoU_this_run_mean_avg = np.mean([
        data1['highest_IoU_this_run']['mean'],
        data2['highest_IoU_this_run']['mean'],
        data3['highest_IoU_this_run']['mean']
    ])

    highest_IoU_this_run_stdev_avg = np.mean([
        data1['highest_IoU_this_run']['stdev'],
        data2['highest_IoU_this_run']['stdev'],
        data3['highest_IoU_this_run']['stdev']
    ])

    highest_IoU_this_run_quantiles_avg = np.mean([
        data1['highest_IoU_this_run']['quantiles'],
        data2['highest_IoU_this_run']['quantiles'],
        data3['highest_IoU_this_run']['quantiles']
    ], axis=0).tolist()

    original_annotations_per_image_this_run_mean_avg = np.mean([
        data1['original_annotations_per_image_this_run']['mean'],
        data2['original_annotations_per_image_this_run']['mean'],
        data3['original_annotations_per_image_this_run']['mean']
    ])

    original_annotations_per_image_this_run_stdev_avg = np.mean([
        data1['original_annotations_per_image_this_run']['stdev'],
        data2['original_annotations_per_image_this_run']['stdev'],
        data3['original_annotations_per_image_this_run']['stdev']
    ])

    original_annotations_per_image_this_run_quantiles_avg = np.mean([
        data1['original_annotations_per_image_this_run']['quantiles'],
        data2['original_annotations_per_image_this_run']['quantiles'],
        data3['original_annotations_per_image_this_run']['quantiles']
    ], axis=0).tolist()

    areas_mean_avg = np.mean([
        data1['areas']['mean'],
        data2['areas']['mean'],
        data3['areas']['mean']
    ])

    areas_stdev_avg = np.mean([
        data1['areas']['stdev'],
        data2['areas']['stdev'],
        data3['areas']['stdev']
    ])

    areas_quantiles_avg = np.mean([
        data1['areas']['quantiles'],
        data2['areas']['quantiles'],
        data3['areas']['quantiles']
    ], axis=0).tolist()

    highest_IoU_mean_avg = np.mean([
        data1['highest_IoU']['mean'],
        data2['highest_IoU']['mean'],
        data3['highest_IoU']['mean']
    ])

    highest_IoU_stdev_avg = np.mean([
        data1['highest_IoU']['stdev'],
        data2['highest_IoU']['stdev'],
        data3['highest_IoU']['stdev']
    ])

    highest_IoU_quantiles_avg = np.mean([
        data1['highest_IoU']['quantiles'],
        data2['highest_IoU']['quantiles'],
        data3['highest_IoU']['quantiles']
    ], axis=0).tolist()

    original_annotations_per_image_mean_avg = np.mean([
        data1['original_annotations_per_image']['mean'],
        data2['original_annotations_per_image']['mean'],
        data3['original_annotations_per_image']['mean']
    ])

    original_annotations_per_image_stdev_avg = np.mean([
        data1['original_annotations_per_image']['stdev'],
        data2['original_annotations_per_image']['stdev'],
        data3['original_annotations_per_image']['stdev']
    ])

    original_annotations_per_image_quantiles_avg = np.mean([
        data1['original_annotations_per_image']['quantiles'],
        data2['original_annotations_per_image']['quantiles'],
        data3['original_annotations_per_image']['quantiles']
    ], axis=0).tolist()

    # write to file
    os.makedirs('./results/type2noise', exist_ok=True)
    with open(os.path.join('./results/type2noise', f'average_stats{i}.txt'), 'w') as f:
        f.write(f"annotations_per_class_this_run_avg: {annotations_per_class_this_run_avg}\n")
        f.write(f"annotations_per_class_avg: {annotations_per_class_avg}\n")
        f.write(f"areas_this_run_mean_avg: {areas_this_run_mean_avg}\n")
        f.write(f"areas_this_run_stdev_avg: {areas_this_run_stdev_avg}\n")
        f.write(f"areas_this_run_quantiles_avg: {areas_this_run_quantiles_avg}\n")
        f.write(f"highest_IoU_this_run_mean_avg: {highest_IoU_this_run_mean_avg}\n")
        f.write(f"highest_IoU_this_run_stdev_avg: {highest_IoU_this_run_stdev_avg}\n")
        f.write(f"highest_IoU_this_run_quantiles_avg: {highest_IoU_this_run_quantiles_avg}\n")
        f.write(f"original_annotations_per_image_this_run_mean_avg: {original_annotations_per_image_this_run_mean_avg}\n")
        f.write(f"original_annotations_per_image_this_run_stdev_avg: {original_annotations_per_image_this_run_stdev_avg}\n")
        f.write(f"original_annotations_per_image_this_run_quantiles_avg: {original_annotations_per_image_this_run_quantiles_avg}\n")
        f.write(f"areas_mean_avg: {areas_mean_avg}\n")
        f.write(f"areas_stdev_avg: {areas_stdev_avg}\n")
        f.write(f"areas_quantiles_avg: {areas_quantiles_avg}\n")
        f.write(f"highest_IoU_mean_avg: {highest_IoU_mean_avg}\n")
        f.write(f"highest_IoU_stdev_avg: {highest_IoU_stdev_avg}\n")
        f.write(f"highest_IoU_quantiles_avg: {highest_IoU_quantiles_avg}\n")
        f.write(f"original_annotations_per_image_mean_avg: {original_annotations_per_image_mean_avg}\n")
        f.write(f"original_annotations_per_image_stdev_avg: {original_annotations_per_image_stdev_avg}\n")
        f.write(f"original_annotations_per_image_quantiles_avg: {original_annotations_per_image_quantiles_avg}\n")

