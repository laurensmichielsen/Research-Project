import os

def generate_metrics(mp, mr, mAP, map50, map55, map60, map65, map70, map75, map80, map85, map90, map95, filename, target_location, percentage_of_noise):
    # write the metrics to a txt file in the following format remember that mAp_at_IoU_tresholds is a list, if the file already exists but it at the bottom:
    with open(os.path.join(target_location, filename), 'a') as file:
        file.write(f'{percentage_of_noise} {mp} {mr} {mAP} {map50} {map55} {map60} {map65} {map70} {map75} {map80} {map85} {map90} {map95}\n')

def generate_metrics_faster_rcnn(mAP, map50, map75, mAP_per_class, filename, target_location, percentage_of_noise):
    # write the metrics to a txt file in the following format remember that mAp_at_IoU_tresholds is a list, if the file already exists but it at the bottom:
    with open(os.path.join(target_location, filename), 'a') as file:
        file.write(f'{percentage_of_noise} {str(mAP)} {str(map50)} {str(map75)} {str(mAP_per_class)}\n')