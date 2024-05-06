'''
Date: 2024-03-19 23:16:07
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-05-04 19:42:25
FilePath: \Graduation_Project\核心代码\Analytical_model.py
'''
import os
import zipfile
import cv2
from creat_CSV_file import CreateCSVFile
from VectorNeuralNetworks import create_neural_network
from manage_model import model_is_OK


def unzip_file(file_name, file_path):
    extract_to = file_path.split('.')[0]
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def check_model(file_path):
    picture_path = os.path.join(file_path.split('.')[0], 'picture')
    videos_path = os.path.join(file_path.split('.')[0], 'videos')
    items = os.listdir(picture_path)
    picture_files = [
        item for item in items
        if os.path.isfile(os.path.join(picture_path, item))
    ]
    items = os.listdir(videos_path)
    videos_files = [
        item for item in items
        if os.path.isfile(os.path.join(videos_path, item))
    ]
    for i in range(len(picture_files)):
        picture_files[i] = picture_files[i].split('.')[0]
    for i in range(len(videos_files)):
        videos_files[i] = videos_files[i].split('.')[0]
    picture_files_set = set(picture_files)
    videos_files_set = set(videos_files)
    if picture_files_set == videos_files_set:
        return True
    else:
        return False


def extract_frames(videos_name, video_path):
    output_folder = os.path.join(video_path, 'frame',
                                 videos_name.split('.')[0])
    video_path = os.path.join(video_path, 'videos', videos_name)
    videos_name = videos_name.split('.')[0]
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 读取视频帧并保存为图像文件
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 保存帧为图像文件
        frame_path = os.path.join(output_folder,
                                  f"{videos_name}_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    # 关闭视频文件
    cap.release()


def select_video(file_path):
    videos_path = os.path.join(file_path.split('.')[0], 'videos')
    items = os.listdir(videos_path)
    videos_name = [
        item for item in items
        if os.path.isfile(os.path.join(videos_path, item))
    ]
    video_path = file_path.split('.')[0]
    for i in range(len(videos_name)):
        extract_frames(videos_name[i], video_path)


def get_file_name(file_path):
    picture_path = os.path.join(file_path.split('.')[0], 'picture')
    items = os.listdir(picture_path)
    picture_files = [
        item for item in items
        if os.path.isfile(os.path.join(picture_path, item))
    ]
    for i in range(len(picture_files)):
        picture_files[i] = picture_files[i].split('.')[0]
    return picture_files


def start_Analytical_model(file_name, file_path):
    #file_name是含.zip的
    unzip_file(file_name, file_path)
    print('模型解压完成')
    check_model(file_path)
    print('模型校验完成')
    select_video(file_path)
    print('模型切割完成')
    CreateCSVFile(get_file_name(file_path), file_path.split('.')[0], file_name)
    print('数据集准备完成')
    network_path = create_neural_network(
        file_name.split('.')[0], get_file_name(file_path),
        os.path.join(
            file_path.split('.')[0], f"{file_name.split('.')[0]}.csv"))
    print('神经网络训练完成', network_path)
    model_is_OK(file_name.split('.')[0])


def Analytical_model(file_name):
    if (file_name.split('.')[1] == 'zip'):
        file_path = os.path.join(os.getcwd(), 'MyModels',
                                 file_name.split('.')[0], file_name)
        start_Analytical_model(file_name, file_path)
    else:
        return False


if __name__ == '__main__':
    name = 'number_model.zip'
    Analytical_model(name)
