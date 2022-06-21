import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = 'database-1.cnd2fqwu3b8i.ap-northeast-2.rds.amazonaws.com',
        database = 'Schedule',
        user = 'memo_user1',
        password = 'memo1234'
    )
    return connection