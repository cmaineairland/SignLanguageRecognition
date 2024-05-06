'''
Date: 2023-11-26 11:37:05
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-04-25 23:09:38
FilePath: \Graduation_Project\核心代码\predict.py
'''


def predict(vector, LabelList, net_path):
    import torch
    net = torch.load(net_path)
    if (vector == 0 or vector == -1):
        return None
    else:
        output = net(torch.Tensor(vector).to(torch.float32))
        PreLabel = torch.argmax(output, dim=0)
        PreLabel = PreLabel.numpy().tolist()
        return LabelList[PreLabel]


if __name__ == '__main__':
    LabelList = ['1', '2']
    from get_hand_key_point_from_image import get_hand_key_point
    path = "MyModels/number_model/number_model/2.jpg"
    net_path = 'MyModels/number_model/number_model/NetWork.pth'
    vector = get_hand_key_point(path)
    print(predict(vector, LabelList, net_path))
