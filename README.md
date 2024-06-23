# Research-Project
The annotation effort associated with object detection is extremely costly. One option to reduce cost is to relax the demands on annotation quality, effectively allowing annotation noise. Current research primarily focuses on noise correction before or during training. However, there remains a gap in the research regarding the impact of specific types of human annotation noise on object-detector performance. This research aimed to determine how sensitive object detectors are to human annotation noise. A systematic methodology was developed to generate and quantify the effects of four noise types: missing annotations, extra annotations, inaccurate bounding boxes, and wrong classification labels. Additionally, evaluations were conducted on YOLOv8 and Faster R-CNN using the PASCAL VOC 2012, VisDrone, and Brain-Tumor datasets. The experiments demonstrated that adding noise to smaller datasets adversely affects the performance of object detectors trained on these datasets more than it does for those trained on larger datasets. Similarly, annotation noise in small objects affects detector performance more than large objects. Furthermore, YOLOv8 is resilient to low levels of missing annotations and inaccurate bounding boxes but is sensitive to all levels of incorrect classification labels. Interestingly, extra annotations seem to have a regularization effect on YOLOv8. In contrast, Faster R-CNN is generally more susceptible to annotation noise compared to YOLOv8, particularly concerning extra annotations, though both models display similar trends regarding inaccurate bounding boxes.

## Experiments
The experiments were conducted on three datasets: PASCAL VOC 2012, VisDrone, and Brain-Tumor. The annotation noise was generated by introducing four types of noise: missing annotations, extra annotations, inaccurate bounding boxes, and wrong classification labels. The experiments were conducted on two object detectors: YOLOv8 and Faster R-CNN. The experiments were conducted on both small and large objects to determine the impact of object size on detector performance. The experiments were conducted on both small and large datasets to determine the impact of dataset size on detector performance.

## Reproducing the Experiments
To reproduce the experiments, follow the steps below:
1. Clone the repository
2. Download the datasets from the following links:
    - [PASCAL VOC 2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/)
    - [VisDrone](https://github.com/VisDrone/VisDrone-Dataset)
    - [Brain-Tumor](https://docs.ultralytics.com/datasets/detect/brain-tumor/)

3. Create a folder named `datasets` in the root directory of the repository and make three subfolders named `PASCAL_VOC_2012`, `VisDrone`, and `Brain_Tumor`.
4. For each dataset create the following structure
```
datasets
│-- PASCAL_VOC_2012
│   │-- AllLabels
│   │-- AllImages
│   │-- images
│   │---- train
│   │---- val
│   │---- test
│   │-- labels
│   │---- train
│   │---- val
│   │---- test
│   │-- noise1
│   │---- labels
│   │---- images
│   │-- noise
```
Collect all the images and labels and make sure they are in YOLO format.
5. Run the experiments by running the files found in the experiments folder. You can change the datasets and noise types by changing the variables in the files.
6. The results will be saved in the results folder.

