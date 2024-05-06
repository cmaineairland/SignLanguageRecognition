'''
Date: 2023-11-06 00:14:31
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-04-25 22:46:28
FilePath: \Graduation_Project\核心代码\GetLabelVector.py
'''


def GetLabelVector(label, LabelList):
    Vector = [[0 for i in range(len(LabelList))] for i in range(len(label))]
    for i in range(len(label)):
        Vector[i][LabelList.index(label[i])] = 1
    return Vector


if __name__ == '__main__':
    # 示例标签列表
    LabelList = ['1', '2']

    # 调用函数并传入标签列表
    label = [
        '1', '1', '2', '1', '2', '1', '1', '2', '1', '2', '2', '2', '2', '1',
        '1', '2', '1', '1', '2', '1', '1', '1', '1', '2', '1', '2', '2', '2',
        '1', '1', '1', '2'
    ]
    vector = GetLabelVector(label, LabelList)
    print(vector)
