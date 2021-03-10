# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
import os
from glob import glob
import pandas as pd



# target_label_file_name = 'classmap.csv'

target_label_file_path = './classmap.csv'
# Opening a file using "with" is as simple as: with open(filename) as file:
# 在 f 資料夾讀一筆，則 .splitlines():返回一個包含各列作為元素的列表，然後 line.split(', ') 代表用 ', ' 分隔相鄰列表
with open(target_label_file_path) as f:
    all_lines = [line.split(',') for line in f.read().splitlines()]
    
all_lines = all_lines[1::]
# 將list 換成dic的形式
target_labels = dict()
for line in all_lines:
    target_class, target_label = line
    target_labels[target_class] = target_label


# 指定存放 train 資料集的資料夾
train_dir = "./training_set"
img_path_list = []
img_class_list = []
# 利用迴圈依序用字典的 key 找出該類別(key)的路徑，再透過 glob() 找出路徑下的所有文件，
# 並透過迴圈每找到一個文件，就在 img_class_list 裡增加一個該類的的 label
for key in target_labels.keys():
    for file_path in glob('{}/{}/*.jpg'.format(train_dir, key)):     # glob: 返回所有匹配的文件路徑列表
        img_class_list.append(target_labels[key])                    # {}.format() : 將()裡的東西，變成{}形式的字串
        img_path_list.append(file_path)

data_list = pd.DataFrame({'class': img_class_list, 'path': img_path_list})





# 查看類別資料夾裡的資料
result = []
image_li = data_list.path.tolist()
for i in range(len(image_li)):
    # 讀取圖檔
    img = cv2.imread(image_li[i])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)




    img = cv2.resize(img,(675, 900))


    # 裁切區域的 x 與 y 座標（左上角）
    x = 100
    y = 30

    # 裁切區域的長度與寬度
    w = 525
    h = 770

    # 裁切圖片
    cut_img = img[y:y+h, x:x+w]

    #bgr
    boundaries = [
        ([117, 0, 0], [255, 255, 108]), # blue
    # 	([86, 31, 4], [220, 88, 50]),
    # 	([25, 146, 190], [62, 174, 250]),
    # 	([103, 86, 65], [145, 133, 128])
    ]


    v1_min, v2_min, v3_min = 117, 0, 0
    v1_max, v2_max, v3_max = 255, 255, 108



    find_blue_pixel = cv2.inRange(cut_img, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))


    blue_color = len(find_blue_pixel[find_blue_pixel > 200])/(find_blue_pixel.shape[0]*find_blue_pixel.shape[1])
    result.append(blue_color)
    

    
result = pd.DataFrame(result, columns = ['blue_color'])

data_result_df = pd.concat([data_list, result], axis = 1)
data_result_df.to_csv('./{}.csv'.format(data_result_df))
