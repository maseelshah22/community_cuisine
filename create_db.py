import pymysql


def get_db():
    return pymysql.connect(
        host = 'mysql01.cs.virginia.edu',
        user = 'dda5us',
        password = 'd@t@b@s3',
        database = 'dda5us',
        cursorclass = pymysql.cursors.DictCursor
    )

connection = get_db()
cursor = connection.cursor()
print(connection)
connection.close()