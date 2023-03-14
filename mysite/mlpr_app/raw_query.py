from django.db import connection

def raw_query(SQL):
    cursor = connection.cursor()
    cursor.execute(SQL)
    return cursor.fetchall()