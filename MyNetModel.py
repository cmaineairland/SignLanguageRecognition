'''
Date: 2023-11-05 23:38:08
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2023-11-25 20:56:02
FilePath: \Graduation_Project\MyNetModel.py
'''
import torch


class Net(torch.nn.Module):

    def __init__(self, in_dim, mid_dim, out_dim):
        super().__init__()
        self.fc1 = torch.nn.Linear(in_dim, mid_dim)
        self.fc2 = torch.nn.Linear(mid_dim, mid_dim)
        self.fc3 = torch.nn.Linear(mid_dim, mid_dim)
        self.fc4 = torch.nn.Linear(mid_dim, mid_dim)
        self.fc5 = torch.nn.Linear(mid_dim, out_dim)

    def forward(self, x):
        x = torch.nn.functional.leaky_relu(self.fc1(x))
        x = torch.nn.functional.leaky_relu(self.fc2(x))
        x = torch.nn.functional.leaky_relu(self.fc3(x))
        x = torch.nn.functional.leaky_relu(self.fc4(x))
        x = torch.nn.functional.softmax(self.fc5(x), dim=0)
        return x


if __name__ == '__main__':
    net = Net(2)
    input = torch.FloatTensor([x for x in range(64)])
    print(input)
    output = net(input)
    print(output)
