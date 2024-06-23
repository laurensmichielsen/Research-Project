import os

ids = [39, 40, 41, 42, 43, 44, 45, 56, 57, 60, 67, 68, 69, 70, 71, 72, 74, 75]
def convert_labels_custom_data(labels_folder):
    labels = os.listdir(labels_folder)

    for label in labels:
        lines = []
        with open(os.path.join(labels_folder, label), "r") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            class_id, x_center, y_center, width, height = lines[i].split()
            class_id = int(class_id)
            new_class_id = ids.index(class_id)
            lines[i] = f"{new_class_id} {x_center} {y_center} {width} {height}\n"
        
        with open(os.path.join(labels_folder, label), "w") as f:
            f.writelines(lines)

labels_folder = "./dataset2/AllLabels"

convert_labels_custom_data(labels_folder)