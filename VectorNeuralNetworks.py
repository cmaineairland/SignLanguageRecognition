'''
Date: 2023-10-20 09:26:07
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-04-25 23:08:15
FilePath: \Graduation_Project\核心代码\VectorNeuralNetworks.py
'''

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import MyNetModel
from GetLabelVector import GetLabelVector
import os


class MyDataset(Dataset):

    def __init__(self, df, in_dim):
        # 初始化数据集
        x = [i for i in range(in_dim)]
        for i in range(in_dim):
            x[i] = '{}'.format(x[i])
        self.x_data = df[x].values
        self.y_data = df['label'].values
        self.length = len(self.y_data)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]


def create_neural_network(file_name, LabelList, data_path):
    # file_name代表模型名称
    # LabelList代表手势标签列表
    # data_path代表数据集路径

    # 定义神经网络的输入、中间层和输出维度
    in_dim = 41
    mid_dim = 128
    out_dim = len(LabelList)

    # 初始化神经网络模型
    NetWork = MyNetModel.Net(in_dim, mid_dim, out_dim)

    # 读取手势数据集
    HandData = pd.read_csv(data_path)

    # 创建自定义数据集
    HandDataset = MyDataset(HandData, in_dim)

    # 划分训练集和测试集
    TrainSize = int(len(HandDataset) * 0.8)
    TestSize = len(HandDataset) - TrainSize
    TrainDataset, TestDataset = torch.utils.data.random_split(
        HandDataset, [TrainSize, TestSize])

    # 创建数据加载器
    TrainDataLoader = DataLoader(dataset=TrainDataset,
                                 batch_size=32,
                                 shuffle=True,
                                 num_workers=0,
                                 drop_last=True)
    TestDataLoader = DataLoader(dataset=TrainDataset,
                                batch_size=32,
                                shuffle=True,
                                num_workers=0,
                                drop_last=True)

    # 定义损失函数、学习率和优化器
    loss_func = torch.nn.CrossEntropyLoss()
    LearnRate = 0.01
    Optimizer = torch.optim.SGD(NetWork.parameters(), lr=LearnRate)
    total_train_step = 0
    total_test_step = 0

    # 训练轮数
    epoch = 100000000
    for i in range(epoch):
        TrueNum = 0
        total_pre = 0
        CorrectRate = 0
        print("第{}轮开始：".format(i + 1))

        # 训练模型
        for data in TrainDataLoader:
            Vector, label = data
            label = label.tolist()
            label = [str(item) for item in label]
            output = NetWork(Vector.to(torch.float32))
            loss = loss_func(output,
                             torch.Tensor(GetLabelVector(label, LabelList)))
            Optimizer.zero_grad()
            loss.backward()
            Optimizer.step()
            total_train_step = total_train_step + 1

        # 测试模型
        total_test_loss = 0
        with torch.no_grad():
            for data in TestDataLoader:
                Vector, label = data
                label = label.tolist()
                label = [str(item) for item in label]
                output = NetWork(Vector.to(torch.float32))
                PreLabel = output.argmax(1)

                PreLabel = PreLabel.numpy().tolist()
                for j in range(len(PreLabel)):
                    if (LabelList[PreLabel[j]] == label[j]):
                        TrueNum = TrueNum + 1
                    total_pre = total_pre + 1
                loss = loss_func(
                    output, torch.Tensor(GetLabelVector(label, LabelList)))
                total_test_loss = total_test_loss + loss.item()

            # 计算正确率
            Accuracy = TrueNum * 100 / total_pre
            print("当前正确率为：{}%".format(Accuracy))

            # 根据正确率保存模型
            if (TrueNum / total_pre >= 0.8):
                network_path = os.path.join(os.path.dirname(data_path),
                                            "NetWork.pth")
                torch.save(NetWork, network_path)
                print('第{}轮正确率大于80%，网络模型已保存'.format(i + 1))
                return network_path
