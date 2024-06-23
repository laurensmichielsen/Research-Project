import os

yolo_path = "./YOLO"

yolo_files = os.listdir(yolo_path)
# Remove all the files that are not .txt files
yolo_files = [file for file in yolo_files if file.endswith('.txt')]

maps_yolo = [[] for _ in range(6)]
for file in yolo_files:
    # get the mAPs from the file
    with open(os.path.join(yolo_path, file), 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.split()
            mAP = float(line[3])
            maps_yolo[i].append(mAP)

# calculate the average of each subarray in maps_yolo
maps_yolo_res = [sum(subarray) / len(subarray) for subarray in maps_yolo]

# get the mAPs from the brain_tumor_folder
brain_tumor_path = "./brain_tumor"
brain_tumor_files = os.listdir(brain_tumor_path)
# Remove all the files that are not .txt files
brain_tumor_files = [file for file in brain_tumor_files if file.endswith('.txt')]
maps_brain_tumor = []
for file in brain_tumor_files:
    # get the mAP from the file
    with open(os.path.join(brain_tumor_path, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            mAP = float(line[3])
            maps_brain_tumor.append(mAP)
print(maps_brain_tumor)
# get the mAPS from the VIS folder
vis_path = "./VIS"
vis_files = os.listdir(vis_path)
# Remove all the files that are not .txt files
vis_files = [file for file in vis_files if file.endswith('.txt')]
maps_vis = []
for file in vis_files:
    # get the mAP from the file
    with open(os.path.join(vis_path, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            mAP = float(line[3])
            maps_vis.append(mAP)
print(maps_vis)
# get the maps from the Faster-RCNN folder
faster_rcnn_path = "./Faster-RCNN"
faster_rcnn_files = os.listdir(faster_rcnn_path)
# Remove all the files that are not .txt files
faster_rcnn_files = [file for file in faster_rcnn_files if file.endswith('.txt')]
maps_faster_rcnn = []
for file in faster_rcnn_files:
    # get the mAP from the fils
    with open(os.path.join(faster_rcnn_path, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            mAP = float(line[1])
            maps_faster_rcnn.append(mAP)

# write the mAPs to a file
with open('mAPs.txt', 'w') as f:
    f.write(f'YOLO: {maps_yolo_res[0]} {maps_yolo_res[1]} {maps_yolo_res[2]} {maps_yolo_res[3]} {maps_yolo_res[4]} {maps_yolo_res[5]}\n')
    f.write(f'Brain Tumor: {maps_brain_tumor[0]} {maps_brain_tumor[1]} {maps_brain_tumor[2]} {maps_brain_tumor[3]} {maps_brain_tumor[4]} {maps_brain_tumor[5]}\n')
    f.write(f'VIS: {maps_vis[0]} {maps_vis[1]} {maps_vis[2]} {maps_vis[3]} {maps_vis[4]} {maps_vis[5]}\n')
    f.write(f'Faster-RCNN: {maps_faster_rcnn[0]} {maps_faster_rcnn[1]} {maps_faster_rcnn[2]} {maps_faster_rcnn[3]} {maps_faster_rcnn[4]} {maps_faster_rcnn[5]}\n')

            