'''
Date: 2024-04-26 20:09:01
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-05-04 18:37:19
FilePath: \Graduation_Project\核心代码\manage_username_password.py
'''
'''
Date: 2024-04-26 20:09:01
LastEditors: Qianshanju
E-mail: z1939784351@gmail.com
LastEditTime: 2024-04-29 23:20:40
FilePath: \Graduation_Project\核心代码\manage_username_password.py
'''
import mysql.connector


def check_username_password(username, password):
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='020710',
                                         database='Graduation_Project')

    cursor = connection.cursor()
    # 执行 SQL 查询
    query = f"SELECT user_password FROM user WHERE user_name = '{username}'"
    cursor.execute(query)
    # 获取查询结果
    rows = cursor.fetchall()
    # 打印查询结果
    if len(rows) == 0:
        return 'account not exist'
    elif rows[0][0] == password:
        return 'success'
    elif rows[0][0] != password:
        return 'password wrong'
    else:
        return 'error'


def create_user(username, password):
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='020710',
                                         database='Graduation_Project')

    cursor = connection.cursor()
    query = f"SELECT user_name FROM user WHERE user_name = '{username}'"
    cursor.execute(query)
    # 获取查询结果
    rows = cursor.fetchall()
    if len(rows) > 0:
        return 'account exists'
    else:
        insert_query = f"INSERT INTO user (user_name, user_password) VALUES ('{username}', '{password}')"
        cursor.execute(insert_query)
        connection.commit()
        return 'success'


if __name__ == '__main__':
    username = 'mahui'
    password = '20020110'
    print(create_user(username, password))
