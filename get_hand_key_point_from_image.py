'''
Date: 2023-11-09 14:06:44
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2023-11-26 13:26:42
FilePath: \Graduation_Project\get_hand_key_point_from_image.py
'''
import cv2
import mediapipe as mp
import os
from google.protobuf.json_format import MessageToDict
import numpy


def core(image, is_video=False):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.8)
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    mpDraw = mp.solutions.drawing_utils

    vector = list()
    if (results.multi_hand_landmarks != None):
        object_hand = results.multi_hand_landmarks[0]
        h, w, c = image.shape
        l = pow(h * h + w * w, 0.5)
        if (is_video):
            for i in range(21):
                cx, cy = int(object_hand.landmark[i].x * w), int(
                    object_hand.landmark[i].y * h)
                cv2.circle(image, (cx, cy), int(w / 50), (255, 0, 255), -1)
            mpDraw.draw_landmarks(image, object_hand, mpHands.HAND_CONNECTIONS)
        right_or_left = MessageToDict(
            results.multi_handedness[0])['classification'][0]['label']
        if (right_or_left == 'left'):
            vector.append(-1)
        else:
            vector.append(1)
        for i in range(20):
            vector.append(
                (object_hand.landmark[i + 1].x - object_hand.landmark[0].x) *
                l)
        for i in range(20):
            vector.append(
                (object_hand.landmark[0].y - object_hand.landmark[i + 1].y) *
                l)
        hands.close()
        return vector
    else:
        hands.close()
        return 0
        # 没有检测到手返回0


def get_hand_key_point(key):
    if (type(key) == numpy.ndarray):
        return core(key, is_video=True)
    elif (type(key) == str and os.path.exists(key)):
        image = cv2.imread(key)
        return core(image)
    else:
        return -1
        # 文件不存在返回-1


if __name__ == '__main__':
    path = "DataSet/MyTest/J(left).jpg"
    print(get_hand_key_point(path))
