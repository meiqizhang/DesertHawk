import base64
import os
import time
import datetime

import markdown
import markdown2
import pymysql
from django.conf import settings

#settings.configure()

from DesertHawk.settings import THUMB_URL, BASE_DIR, MEDIA_URL, BLOG_ROOT, DATABASES

def db_connect():
    database = DATABASES.get("default")

    from_cnn= pymysql.Connect(
        host=database['HOST'],
        port=int(database['PORT']),
        user=database['USER'],
        passwd=database['PASSWORD'],
        db="zhqiBlog",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    to_cnn= pymysql.Connect(
        host=database['HOST'],
        port=int(database['PORT']),
        user=database['USER'],
        passwd=database['PASSWORD'],
        db="desert_hawk",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return from_cnn, to_cnn


def migrate_tags():
    from_cnn, to_cnn = db_connect()
    from_cursor = from_cnn.cursor()
    to_cursor = to_cnn.cursor()
    from_sql = "select tags from t_article"
    row = from_cursor.execute(from_sql)
    records = from_cursor.fetchall()
    all_tags = set()
    for i in range(row):
        tags = records[i]["tags"]
        try:
            tags = eval(tags)
        except Exception as e:
            tags = tags.split(";")
        if isinstance(tags, list):
            all_tags = set(list(all_tags) + tags)
    for tag in all_tags:
        try:
            to_sql = "insert into t_tag (`tag`) values(%s)"
            to_cursor.execute(to_sql, tag)
            to_cnn.commit()
        except Exception as e:
            print(e)
 
def migrate_article():
    # 建立游标
    from_cnn, to_cnn = db_connect()
    from_cursor = from_cnn.cursor()
    to_cursor = to_cnn.cursor()
    
    tag_sql = "select * from t_tag"
    row = to_cursor.execute(tag_sql)
    records = to_cursor.fetchall()
    tag_id_map = dict()
    for i in range(row):
        idx = records[i]["id"]
        tag = records[i]["tag"]
        tag_id_map[tag] = idx
 
    from_sql = "select * from t_article"
    row = from_cursor.execute(from_sql)
    records = from_cursor.fetchall()
    for i in range(row):
        line = records[i]
        print(line["article_id"], line["title"])
        to_sql = "insert t_article(`article_id`, `title`, `abstract`, `content`, `date`, `click_num`, `love_num`, `status`, `category_id`, `cover_id`)" \
                 "values(%s, %s, %s, %s, %s, %s, '0', 'p', '1', '1')"

        try:
            to_cursor.execute(to_sql, (line["article_id"], line["title"], line["description"], line["content"], line["date"], line["click_num"]))
            to_cnn.commit()
        except Exception as e:
            print(e)

def migrate_ipcoordinate():
    from_cnn, to_cnn = db_connect()
    from_cursor = from_cnn.cursor()
    to_cursor = to_cnn.cursor()
    from_sql = "select * from t_site_statistic"
    row = from_cursor.execute(from_sql)
    records = from_cursor.fetchall()
    for i in range(row):
        line = records[i]
        ip_str = line["ip_str"]
        if ip_str.strip() == "220.114.194.2":
            print(line)
        else:
            continue
        #to_sql = "insert into t_ip_coordinate (`ip_str`, `province`, `city`, `x`, `y`) values('%s', '%s', '%s', '%s', '%s')" 
        #args = (line["ip_str"], line["province"], line["city"], line["x"], line["y"])
        to_sql = "insert into t_ip_coordinate (`ip_str`, `province`, `city`, `x`, `y`) values('%s', '%s', '%s', '%s', '%s')"  %  (line["ip_str"], line["province"], line["city"], line["x"], line["y"])
        try:
            to_cursor.execute(to_sql)
            to_cnn.commit()
        except Exception as e:
            pass
            print(e, to_sql)


def migrate_statistic():
    from_cnn, to_cnn = db_connect()
    from_cursor = from_cnn.cursor()
    to_cursor = to_cnn.cursor()

    coordinate_sql = "select * from t_ip_coordinate"
    row = to_cursor.execute(coordinate_sql)
    records = to_cursor.fetchall()
    coordinate_id_map = dict()
    for i in range(row):
        line = records[i]
        coordinate_id_map[line["ip_str"]] = line['id']

    #ips = coordinate_id_map.keys()
    #print('220.114.194.2' in ips)
    #print(coordinate_id_map['220.114.194.2'])
    #return

    from_sql = "select * from  t_visit_history"
    row = from_cursor.execute(from_sql)
    records = from_cursor.fetchall()
    for i in range(row):
        line = records[i]
        ip_str = line["ip_str"]
        if ip_str not in coordinate_id_map:
            continue
        to_sql = "insert into t_site_statistic(`url`, `visit_time`, `coordinate_id`) values(%s, %s, %s)"
        print(ip_str)
        args = (line["url"], line["visit_time"], coordinate_id_map[ip_str])
        to_cursor.execute(to_sql, args)
        to_cnn.commit()

    pass

if '__main__' == __name__:
    #migrate_tags()
    #migrate_article()
    #migrate_ipcoordinate()
    migrate_statistic()
