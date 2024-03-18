import pymysql
from flask import Flask

connection = pymysql.connect(host="localhost", port=3306, 
                             user="cs4650user", password="d@t@b@s3", database="test")
cursor = connection.cursor()
# some other statements  with the help of cursor
print(connection)
connection.close()

# def get_db():
#     return pymysql.connect(
#         host='mysql01.cs.virginia.edu',
#         user='dda5us',
#         password='d@t@b@s3',
#         database='dda5us',
#         cursorclass=pymysql.cursors.DictCursor
#     )

# with get_db() as connection: 
#     with connection.cursor() as cursor:
#         query = 'SELECT * FROM candy'
#         cursor.execute(query)
#         ans = cursor.fetchall()
#         print(ans)

