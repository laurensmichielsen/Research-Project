# import os 
# for file in os.listdir('./data/PASCAL/labels/train'):
#     with open (os.path.join('./data/PASCAL/labels/train', file), 'r') as f:
#         lines = f.readlines()
#         f.close()
#     if len(lines) == 0:
#         print(file)
import os

annotation_files = os.listdir("./datasets/brain-tumor/AllLabels")
total = 0
for file in annotation_files:
    with open(os.path.join("./datasets/brain-tumor/AllLabels", file), 'r') as f:
        lines = f.readlines()
        total += len(lines)

print(total)

images = os.listdir("./datasets/brain-tumor/AllImages")
print(len(images))