import pymysql
from flask import Flask

def get_db():
    return pymysql.connect(
        host='mysql01.cs.virginia.edu',
        user='dda5us',
        password='d@t@b@s3',
        database='dda5us',
        cursorclass=pymysql.cursors.DictCursor
    )

with get_db() as connection: 
    with connection.cursor() as cursor:
        query = 'SELECT * FROM candy'
        cursor.execute(query)
        ans = cursor.fetchall()
        print(ans)


