import base64
import os
import time

import markdown
import markdown2
import pymysql


from DesertHawk.settings import BASE_DIR, MEDIA_URL, BLOG_ROOT, DATABASES

def db_connect():
    database = DATABASES.get("default")

    connect = pymysql.Connect(
        host=database['HOST'],
        port=int(database['PORT']),
        user=database['USER'],
        passwd=database['PASSWORD'],
        db=database['NAME'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connect

def main():
    database = DATABASES.get("default")
    print(database)
    connect = pymysql.Connect(
        host=database['HOST'],
        port=int(database['PORT']),
        user=database['USER'],
        passwd=database['PASSWORD'],
        db=database['NAME'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    # 建立游标
    cursor = connect.cursor()
    #insert_content_image(connect)
    #return
    
    articles = dict()
    sql = "select title, content from t_article"
    cursor.execute(sql)
    for item in cursor.fetchall():
        articles[item["title"]] = item["content"]
        title = item["title"]
        content = item["content"]

        sql = "insert into t_article_index(title, content) values(%s, %s)"
        cursor.execute(sql, (title, content))
    
    connect.commit() 

if '__main__' == __name__:
    main()
