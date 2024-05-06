'''
Date: 2023-11-09 15:27:05
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-04-25 20:45:52
FilePath: \Graduation_Project\核心代码\creat_CSV_file.py
'''
import csv
import os
from get_hand_key_point_from_image import get_hand_key_point
import pyautogui
import random
import time


def CreateCSVFile(FileList, folder_path, file_name):

    CSVHead = ['id'] + [x for x in range(41)] + ['label']
    csv_path = os.path.join(folder_path, f"{file_name.split('.')[0]}.csv")
    f = open(csv_path, "w", encoding='utf-8', newline='')
    csv_write = csv.writer(f)
    csv_write.writerow(CSVHead)
    frame_path = os.path.join(folder_path, 'frame')
    for i in range(0, len(FileList)):
        j = 0
        while True:
            path = os.path.join(frame_path, FileList[i],
                                f'{FileList[i]}_{j}.jpg')
            vector = get_hand_key_point(path)
            if (vector == -1):
                break
            if (vector != 0):
                csv_write.writerow(
                    ([FileList[i] + '_{}'.format(j)] + vector + [FileList[i]]))

            j = j + 1
    f.close()


if __name__ == '__main__':
    FileList = ['1', '2']
    folder_path = os.path.join(os.getcwd(), 'MyModels', 'number_model',
                               'number_model')
    CreateCSVFile(FileList, folder_path, 'number_model.zip')
