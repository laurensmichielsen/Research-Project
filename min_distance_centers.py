import random
import os
import shutil

labels_folder = './data/PASCAL/labels'
def min_distance_between_centers():
    min_distance = 2
    folders = ['test', 'train', 'val']
    for folder in folders:
        labels = os.listdir(os.path.join(labels_folder, folder))
        for label in labels:
            with open(os.path.join(labels_folder, folder, label), 'r') as f:
                lines = f.readlines()
                centers = []
                for line in lines:
                    class_id, x_center, y_center, bbox_width, bbox_height = line.split()
                    centers.append((float(x_center), float(y_center)))
                for i in range(len(centers)):
                    for j in range(i + 1, len(centers)):
                        distance = ((centers[i][0] - centers[j][0]) ** 2 + (centers[i][1] - centers[j][1]) ** 2) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
    print(min_distance)

min_distance_between_centers()
