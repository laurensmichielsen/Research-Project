import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchmetrics.detection.mean_ap import MeanAveragePrecision


from frcnn import FasterRCNN
from LossLogger import LossLogger
from dataset import Pascal


noise_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
seeds = [1, 2, 3, 4, 5, 6]

labels_folder = "./data/PASCAL/labels"
images_folder = "./data/PASCAL/images"

backup_labels_folder = "./data/PASCAL/noise2"

def calculate_mAP_detection(predictions, targets):
    metric = MeanAveragePrecision(class_metrics=True)
    metric.update(predictions, targets)
    return metric.compute()


def experiment(number_of_epochs, generate_noise):
    for j in range(0, len(noise_levels)):
        noise_level = noise_levels[j]
        torch.cuda.empty_cache()
        if j > 0:
            generate_noise(os.path.join(labels_folder, "train"), backup_labels_folder, seed, total_annotations=total_annotations)

        # create and train the model
        # transform
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.TrivialAugmentWide(),
            transforms.ToTensor()
        ])
        # datasets and dataloaders
        train_images = os.listdir(os.path.join(images_folder, "train"))
        train_annotations = os.listdir(os.path.join(labels_folder, "train"))
        train_set = Pascal(train_images, train_annotations, os.path.join(labels_folder, "train"), os.path.join(images_folder, "train"), transform=transform)
        train_loader = DataLoader(train_set, batch_size=16, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

        val_images = os.listdir(os.path.join(images_folder, "val"))
        val_annotations = os.listdir(os.path.join(labels_folder, "val"))
        val_set = Pascal(val_images, val_annotations, os.path.join(labels_folder, "val"), os.path.join(images_folder, "val"), transform=transform)
        val_loader = DataLoader(val_set, batch_size=16, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

        test_images = os.listdir(os.path.join(images_folder, "test"))
        test_annotations = os.listdir(os.path.join(labels_folder, "test"))
        test_set = Pascal(test_images, test_annotations, os.path.join(labels_folder, "test"), os.path.join(images_folder, "test"), transform=transform)
        test_loader = DataLoader(test_set, batch_size=1, shuffle=False, collate_fn=lambda x: tuple(zip(*x)))

        loss_logger = LossLogger(f'./logs/Faster_rcnn/exp1/noise_{noise_level}.csv')

        model = FasterRCNN(num_classes=21, model_path=f'/FCNN-models/exp1/run_0_noise{noise_level}.pth')
        model.train_model(data_loader_train=train_loader, data_loader_val=val_loader, num_epochs=number_of_epochs, loss_logger=loss_logger)

        # test the model
        targets =  [test_set.__getitem__(i)[1] for i in range(test_set.__len__())]
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        predictions = model.evaluate_model(data_loader=test_loader)

        predictions = filter_predictions(predictions, 0.5)

        detection_map = calculate_mAP_detection(predictions, targets)

        # TODO write predictions to file
        print(detection_map)
