import os
import json
import numpy as np

stat_files = os.listdir('./')
stat_files = [file for file in stat_files if file.endswith('.json')]

data = []
for file in stat_files:
    with open(file, 'r') as f:
        data.append(json.load(f))

# Calculate the averages for each run
for i in range(5):
    data1 = data[0][i]
    data2 = data[1][i]
    data3 = data[2][i]
    
    # Calculate the averages for the lists
    annotations_removed_per_class_this_run_avg = np.mean([
        data1['annotations_removed_per_class_this_run'], 
        data2['annotations_removed_per_class_this_run'], 
        data3['annotations_removed_per_class_this_run']
    ], axis=0).tolist()
    
    areas_removed_this_run_quantiles_avg = np.mean([
        data1['areas_removed_this_run']['quantiles'], 
        data2['areas_removed_this_run']['quantiles'], 
        data3['areas_removed_this_run']['quantiles']
    ], axis=0).tolist()
    
    original_annotations_this_run_quantiles_avg = np.mean([
        data1['original_annotations_this_run']['quantiles'], 
        data2['original_annotations_this_run']['quantiles'], 
        data3['original_annotations_this_run']['quantiles']
    ], axis=0).tolist()
    
    annotations_removed_per_class_avg = np.mean([
        data1['annotations_removed_per_class'], 
        data2['annotations_removed_per_class'], 
        data3['annotations_removed_per_class']
    ], axis=0).tolist()
    
    areas_removed_quantiles_avg = np.mean([
        data1['areas_removed']['quantiles'], 
        data2['areas_removed']['quantiles'], 
        data3['areas_removed']['quantiles']
    ], axis=0).tolist()
    
    original_annotations_quantiles_avg = np.mean([
        data1['original_annotations']['quantiles'], 
        data2['original_annotations']['quantiles'], 
        data3['original_annotations']['quantiles']
    ], axis=0).tolist()
    
    # Calculate the averages for scalar values
    areas_removed_this_run_mean_avg = np.mean([
        data1['areas_removed_this_run']['mean'], 
        data2['areas_removed_this_run']['mean'], 
        data3['areas_removed_this_run']['mean']
    ])
    areas_removed_this_run_stdev_avg = np.mean([
        data1['areas_removed_this_run']['stdev'], 
        data2['areas_removed_this_run']['stdev'], 
        data3['areas_removed_this_run']['stdev']
    ])
    
    original_annotations_this_run_mean_avg = np.mean([
        data1['original_annotations_this_run']['mean'], 
        data2['original_annotations_this_run']['mean'], 
        data3['original_annotations_this_run']['mean']
    ])
    original_annotations_this_run_stdev_avg = np.mean([
        data1['original_annotations_this_run']['stdev'], 
        data2['original_annotations_this_run']['stdev'], 
        data3['original_annotations_this_run']['stdev']
    ])
    
    areas_removed_mean_avg = np.mean([
        data1['areas_removed']['mean'], 
        data2['areas_removed']['mean'], 
        data3['areas_removed']['mean']
    ])
    areas_removed_stdev_avg = np.mean([
        data1['areas_removed']['stdev'], 
        data2['areas_removed']['stdev'], 
        data3['areas_removed']['stdev']
    ])
    
    original_annotations_mean_avg = np.mean([
        data1['original_annotations']['mean'], 
        data2['original_annotations']['mean'], 
        data3['original_annotations']['mean']
    ])
    original_annotations_stdev_avg = np.mean([
        data1['original_annotations']['stdev'], 
        data2['original_annotations']['stdev'], 
        data3['original_annotations']['stdev']
    ])
    
    # Write the averages to a text file
    os.makedirs('./results/type1noise', exist_ok=True)
    with open(os.path.join('./results/type1noise', f'average_stats{i}.txt'), 'w') as f:
        f.write(f'annotations_removed_per_class_this_run_avg: {annotations_removed_per_class_this_run_avg}\n')
        f.write(f'areas_removed_this_run_mean_avg: {areas_removed_this_run_mean_avg}\n')
        f.write(f'areas_removed_this_run_stdev_avg: {areas_removed_this_run_stdev_avg}\n')
        f.write(f'areas_removed_this_run_quantiles_avg: {areas_removed_this_run_quantiles_avg}\n')
        f.write(f'original_annotations_this_run_mean_avg: {original_annotations_this_run_mean_avg}\n')
        f.write(f'original_annotations_this_run_stdev_avg: {original_annotations_this_run_stdev_avg}\n')
        f.write(f'original_annotations_this_run_quantiles_avg: {original_annotations_this_run_quantiles_avg}\n')
        f.write(f'annotations_removed_per_class_avg: {annotations_removed_per_class_avg}\n')
        f.write(f'areas_removed_mean_avg: {areas_removed_mean_avg}\n')
        f.write(f'areas_removed_stdev_avg: {areas_removed_stdev_avg}\n')
        f.write(f'areas_removed_quantiles_avg: {areas_removed_quantiles_avg}\n')
        f.write(f'original_annotations_mean_avg: {original_annotations_mean_avg}\n')
        f.write(f'original_annotations_stdev_avg: {original_annotations_stdev_avg}\n')
        f.write(f'original_annotations_quantiles_avg: {original_annotations_quantiles_avg}\n')
