from ultralytics import YOLO
import split
from generate_noise_type1 import generate_noise_type1, collect_labels_and_images
import shutil
import generate_metrics
import zipfile
import os

images_folder = './data/PASCAL/images'
labels_folder = './data/PASCAL/labels'
all_images_folder = './data/AllImages'
all_labels_folder = './data/AllLabels'
backup_images_folder = './data/PASCAL/noise1/images'
backup_labels_folder = './data/PASCAL/noise1/labels'
folder_dir = './results/type1noise'
folder_to_zip = '/content/experiment/Research'
folder_to_store_zip = '/content/drive/MyDrive'
zip_folder_dir = '/content/drive/MyDrive/Results/type1noise'
noise_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
def experiment1(number_of_epochs, number_of_runs):    
    for i in range(number_of_runs):
        split.create_data_split(all_images_folder, all_labels_folder, images_folder, labels_folder)
        for noise_level in noise_levels:
            model = YOLO('yolov8s.pt')
            # Determine the seed to be used for this run
            seed = seeds[i * 6 + noise_levels.index(noise_level)]
            # check if noise needs to be generated
            if noise_level != 0:
                generate_noise_type1(labels_folder, images_folder, backup_labels_folder, backup_images_folder, seed)
            # train the model
            model.train(data="pascal.yaml", epochs=number_of_epochs, batch=-1, project="runs/detect/experiment1", name=f"run_{i}_noise_{noise_level}", seed=seed)
            # TODO: evaluate the model and write the results to a file
            results = model.val(data="pascal.yaml", splits="test", batch=-1)
            mp = results.box.mpß
            mr = results.box.mr
            mAP = results.box.map
            all_ap = results.box.all_ap
            all_ap = np.array(all_ap)
            maps_at_tresholds = np.mean(all_ap, axis=0)
            assert maps_at_tresholds.shape == (10,)
            # Save the results to a file using the generate_metrics.py script
            generate_metrics.generate_metrics(mp, mr, mAP, maps_at_tresholds[0], maps_at_tresholds[1], maps_at_tresholds[2], maps_at_tresholds[3], maps_at_tresholds[4], maps_at_tresholds[5], maps_at_tresholds[6], maps_at_tresholds[7], maps_at_tresholds[8], maps_at_tresholds[9], f"run_{i}_exp1.txt", folder_dir, noise_level)
            # create checkpoint for the experiment
            zip_file_path = os.path.join(folder_to_zip, f"exp1_run_{i}_noise_{noise_level}")
            # create zip_folder containing the results
            shutil.make_archive(zip_file_path, 'zip', folder_dir)
            
        collect_labels_and_images(labels_folder, images_folder, backup_labels_folder, backup_images_folder)
        split.collect_labels_and_images()
