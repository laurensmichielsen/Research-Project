import os

labels_folder = "./datasets/brain-tumor/labels"

folders = ["train", "val", "test"]

for folder in folders:
    source_labels_folder = f"./datasets/brain-tumor/labels/{folder}"
    labels = os.listdir(source_labels_folder)
    for label in labels:
        with open(os.path.join(source_labels_folder, label), "r") as f:
            lines = f.readlines()

        # add newline character to the last line
        if len(lines) > 0:
            lines[-1] = lines[-1] + "\n"
        # write the lines to the file
        with open(os.path.join(source_labels_folder, label), "w") as f:
            f.writelines(lines)