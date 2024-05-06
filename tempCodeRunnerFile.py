'''
Date: 2023-11-25 19:14:55
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-05-04 20:01:44
FilePath: \Graduation_Project\核心代码\serves.py
'''
'''
Date: 2023-11-25 19:14:55
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-05-04 15:40:12
FilePath: \Graduation_Project\核心代码\serves.py
'''
from PIL import Image
import io
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO, emit, send
from get_hand_key_point_from_image import get_hand_key_point
import cv2
import time
import predict
import os
import base64
from Analytical_model import Analytical_model
from manage_username_password import check_username_password, create_user
from manage_model import add_model, check_model

sleep_time = 5
now_model_name = 'default_model'
#每过sleep_time秒后识别一次


def get_LabelList():
    use_list = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'z', 'del', 'space',
        'nothing'
    ]
    global now_model_name
    directory = os.path.join(os.getcwd(), 'MyModels', now_model_name,
                             now_model_name)
    file_list = []
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 拼接文件的完整路径
        filepath = os.path.join(directory, filename)
        # 判断路径是否为文件（非文件夹）
        if os.path.isfile(filepath):
            file_list.append(filename.split('.')[0])  # 将文件名添加到列表中
    return file_list
    return use_list


def get_net_path():
    return 'MyModels/default_model/default_model/NetWork.pth'


class VideoCamera(object):

    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def process_frame(self):
        success, image = self.video.read()
        # 在这里处理视频帧
        vector = get_hand_key_point(image)
        char = predict.predict(vector, get_LabelList(), get_net_path())
        if (char == 'del'):
            with open('sentence.txt', "r") as f:  #设置文件对象
                sentence = f.read()
                sentence = sentence[0:-1]
            with open('sentence.txt', "w") as f:
                f.write(sentence)
        else:
            with open('sentence.txt', "a") as f:  #设置文件对象
                if (type(char) == str):
                    if (char == 'space'):
                        char = '_'
                    f.write(char)
        image = cv2.flip(image, 1)
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_frame(self):
        success, image = self.video.read()
        # 在这里处理视频帧
        get_hand_key_point(image)
        image = cv2.flip(image, 1)
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__, static_folder='./static')
socketio = SocketIO(app)


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')


@app.route('/news/kindergarten')  # 主页
def kindergarten():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('kindergarten.html')


@app.route('/news/WTO')  # 主页
def WTO():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('WTO.html')


@app.route('/news/audiologist')  # 主页
def audiologist():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('audiologist.html')


@app.route('/news/poet')  # 主页
def poet():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('poet.html')


@app.route('/news/GCSE')  # 主页
def GCSE():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('GCSE.html')


@app.route('/more_info/article2248')  # 主页
def article2248():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('more_info_article.html')


@app.route('/手语识别')  # 主页
def sign_language_recognition():
    path = 'sentence.txt'  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
    open('sentence.txt', 'w')
    return render_template('recognition.html')


@app.route('/sentence', methods=["GET"])  # 主页
def sentence():
    # jinja2模板，具体格式保存在index.html文件中
    with open('sentence.txt', "r") as f:
        return Response(f.read())


@app.route('/Select_reference_image')
def Select_reference_image():
    img_stream = ''
    char = request.args.__str__()[32:34]
    if (char == 'sp'):
        char = 'space'
    elif (char == 'de'):
        char = 'del'
    else:
        char = char[0:1]
    path = "DataSet/test/asl_alphabet_test/{}_test.jpg".format(char)
    image = cv2.imread(path)
    ret, jpeg = cv2.imencode('.jpg', image)
    img_stream = jpeg.tobytes()
    img_stream = str(base64.b64encode(img_stream), 'utf-8')
    return img_stream


def gen(camera):
    global sleep_time
    check = True
    while True:
        if (check):
            start = time.time()
            check = False
        now = time.time()
        if (now - start >= sleep_time):
            check = True
            frame = camera.process_frame()
        else:
            frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():

    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    folder_name = os.getcwd() + '\\MyModels\\' + file.filename.split(".")[0]
    os.makedirs(folder_name)
    file.save(folder_name + "\\" + file.filename)
    Analytical_model(file.filename)
    # 也可以直接处理文件内容，例如读取内容或者进行其他操作
    # file_content = file.read()

    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/log_in')  # 主页
def log_in():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('log_in.html')


@app.route('/news')  # 主页
def news():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('news.html')


@app.route('/more_info')  # 主页
def more_info():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('more_info.html')


@app.route('/user_center')  # 主页
def user_center():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('user_center.html')


@app.route('/my_model')  # 主页
def my_model():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('my_model.html')


@app.route('/pay_for_us')  # 主页
def pay_for_us():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('pay_for_us.html')


@app.route('/connect_us')  # 主页
def connect_us():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('connect_us.html')


@app.route('/create_account')  # 主页
def create_account():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('/create_account.html')


@app.route('/get_massage', methods=['POST'])
def get_massage():
    # 从 POST 请求中获取 JSON 数据
    data = request.get_json()
    massage_type = data.get('type')
    print('data:', data)
    if massage_type == 'log_in':

        username = data.get('username')
        password = data.get('password')

        message = check_username_password(username, password)

    if massage_type == 'create_account':
        username = data.get('username')
        password = data.get('password')
        message = create_user(username, password)

    if massage_type == 'change_sleep_time':
        global sleep_time
        sleep_time = data.get('new_sleep_time')
        message = 'success'

    if massage_type == 'upload_file':
        username = data.get('username')
        model_name = data.get('model_name')
        model_name = model_name.split('.')[0]
        message = add_model(username, model_name)

    if massage_type == 'check_model_list':
        print(data.get('username'))
        return check_model(data.get('username'))

    return jsonify({'message': message})


if __name__ == '__main__':

    directory = os.path.join(os.getcwd(), 'MyModels', now_model_name,
                             now_model_name)
    file_list = []
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 拼接文件的完整路径
        filepath = os.path.join(directory, filename)
        # 判断路径是否为文件（非文件夹）
        if os.path.isfile(filepath):
            file_list.append(filename.split('.')[0])  # 将文件名添加到列表中
    print(file_list)
    #app.run(debug=True, port=5000)
    print("退出程序")
