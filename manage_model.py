import mysql.connector
import json


def add_model(username, model_name):
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='020710',
                                         database='Graduation_Project')

    cursor = connection.cursor()
    insert_query = f"INSERT INTO model (model_name, model_owner) VALUES ('{model_name}_training', '{username}')"
    cursor.execute(insert_query)
    connection.commit()
    return 'success'


def check_model(username):
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='020710',
                                         database='Graduation_Project')

    cursor = connection.cursor()
    # 执行 SQL 查询
    query = f"SELECT model_name FROM model WHERE model_owner = '{username}' or model_owner = 'everyone'"
    cursor.execute(query)
    # 获取查询结果
    rows = cursor.fetchall()
    # 打印查询结果
    json_dict = {'len': len(rows)}  # 添加列表长度

    # 将列表的元素加入字典中，按照指定的键名 'name_1', 'name_2', 'name_3' 等
    for i, value in enumerate(rows):
        key_name = f'name_{i+1}'  # 根据索引 i 构造键名，从 'name_1' 开始
        json_dict[key_name] = value
    return json_dict


def model_is_OK(model_name):
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='020710',
                                         database='Graduation_Project')

    cursor = connection.cursor()
    query = f"UPDATE model SET model_name = '{model_name}' WHERE model_name = '{model_name}_training'"
    cursor.execute(query)
    connection.commit()


if __name__ == "__main__":

    model_is_OK('number_model')
