import cv2
import os

folder_path = 'Students'
path_list = os.listdir(folder_path)

for path in path_list:
  full_path = os.path.join(folder_path, path)

  img = cv2.imread(full_path)
  resized = cv2.resize(img, (220, 220))
  cv2.imwrite(full_path, resized)