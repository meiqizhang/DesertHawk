import base64
import os
import time

import markdown
import markdown2
import pymysql
from django.conf import settings

#settings.configure()

from DesertHawk.settings import THUMB_URL, BASE_DIR, MEDIA_URL, BLOG_ROOT, DATABASES

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
    #cursor = connect.cursor()
    #insert_content_image(connect)
    #return

    post_path = os.path.join(BLOG_ROOT, "posts")
    print(post_path)

    for fpathe, dirs, fs in os.walk(post_path):
        for f in fs:
            if os.path.isfile(os.path.join(fpathe, f)):
                parse_page(fpathe.replace('\\', '/'), f, connect)
                #exit()
            #DATABASES

def insert_content_image(connect):
    cursor = connect.cursor()
    path_dir = os.path.join(BLOG_ROOT, "posts/images")
    for image in os.listdir(path_dir):
        md5 = image.split('.')[0]

        image_path = os.path.join(path_dir, image)
        if os.path.isfile(image_path):
            print(image_path)
            with open(image_path, "rb") as fp:
                blob = fp.read()
                print(blob)

                sql = "insert into t_content_image (`md5`, `image`) values (%s, %s) ON DUPLICATE KEY UPDATE `image`=%s"
                cursor.execute(sql, (md5, blob, blob))
                connect.commit()

def parse_page(path, name, connect):
    category = path.split('/')[-1]
    cursor = connect.cursor()

    if name.endswith('.md'):
        with open(os.path.join(path, name), 'r', encoding='utf-8') as fp:
            found = False
            while fp.readable():
                line = fp.readline().strip()
                line = line.strip('\n')
                if line == '---' or line == '***':
                    found = True
                    break

            article = dict()
            article['category'] = category

            if name.endswith('.md'):
                title = name[11:-3]
            else:
                title = name[11:-5]

            while found and fp.readable():
                line = fp.readline().strip()
                line = line.strip('\n')
                if len(line) < 1:
                    continue

                if line == '---' or line == '***':
                    break

                sp = line.find(':')
                if sp > 0:
                    article[line[:sp].strip(' ')] = line[sp+1:].strip(' ')
                else:
                    print('%s format error' % path)
                    continue

            if 'tags' in article:
                article['tags'] = eval(article['tags'])
                sql = 'delete from t_tag where title=%s'
                cursor.execute(sql, (article['title']))
                connect.commit()

                for tag in article['tags']:
                    try:
                        sql = "INSERT INTO t_tag (`tag`, `title`) VALUES (%s, %s) "
                        args = (tag, article['title'])
                        cursor.execute(sql, args)
                        connect.commit()
                    except Exception as e:
                        print(e)
                        connect.rollback()
            else:
                article['tags'] = []

            article['content'] = markdown2.markdown(fp.read(0xffffffff).replace("\r\n", '  \n'),
                                                    extras=["code-friendly"])
            '''markdown.markdown(fp.read(0xffffffff).split("---")[2].replace("\r\n", '  \n'),
                                     extensions=['extra',
                                                 'codehilite',
                                                 'toc',
                                                 ])
             '''

            article['date'] = name[:10]

            if 'title' not in article:
                article['title'] = title

            elif article['title'] != title:
                print("title not same, %s" % title)

            article['title'] = title

            thumb_image = BASE_DIR + MEDIA_URL + THUMB_URL + article['title'] + '.jpg'

            if not os.path.exists(thumb_image): # 图片不存在，查看分类图片
                thumb_image = BASE_DIR + MEDIA_URL + THUMB_URL + article["category"] + '.jpg'
                if not os.path.exists(thumb_image):  # 分类图片不存在，用默认图标
                    thumb_image = BASE_DIR + MEDIA_URL + THUMB_URL + 'default.jpg'

            try:
                with open(thumb_image, "rb") as img:
                    image = img.read()
            except Exception as e:
                print(e)
                image = ''

            sql = "insert into t_article(title, first_category, second_category, tags, description, content, `date`, image) values " \
                  "(%s, '程序设计', %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                  "first_category='程序设计', second_category=%s, tags=%s, description=%s, content=%s, `date`=%s, image=%s"

            args = (article['title'], article['category'], str(article['tags']), article['description'], article['content'], article['date'], image,
                                      article['category'], str(article['tags']), article['description'], article['content'], article['date'], image)

            try:
                cursor.execute(sql, args)
                connect.commit()
            except Exception as e:
                print(e)
                connect.rollback()

if '__main__' == __name__:
    main()
