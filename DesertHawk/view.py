import datetime
import hashlib
import json
import os
import socket
import struct
import uuid

import pymysql
from django.core.files.storage import Storage
from django.http import HttpResponse
from django.shortcuts import render
from qcloud_cos import CosConfig, CosS3Client

from apps.articles.models import ContentImage
from DesertHawk.settings import START_TIME, BLOG_ROOT, DATABASES
from django.views.decorators.csrf import csrf_exempt


def calendar(request):
    return render(request, 'calendar.html')


def about_me(request):
    return render(request, "about.html")

def get_start_time(request):
    print(START_TIME)
    return HttpResponse(START_TIME)

def index(request):
    return render(request, 'index.html')  # 只返回页面，数据全部通过ajax获取

def content_image(request):
    md5 = request.GET.get('md5')

    record = ContentImage.objects.filter(md5=md5).values("image").first()
    response = dict()

    if record:
        image = record['image']
        response["status"] = "success"
        response["image"] = image
    else:
        response["status"] = "error"

    return HttpResponse(response["image"])

@csrf_exempt
def content_image_manager(request):
    if request.method == 'GET':
        print("download image")
        md5 = request.GET.get('md5', '')

        if md5 and len(md5) > 0:
            response = dict()
            record = ContentImage.objects.filter(md5=md5).values("image").first()
            if record:
                image = record['image']
            else:
                print("not found md5=%s image" % md5)
                image = ''

            return HttpResponse(image)

    elif request.method == 'POST':
        print("upload image")
        image_meta = request.FILES.get('fafafa')
        image_name = image_meta.name
        image_size = image_meta.size
        image_buffer = image_meta.read()

        response = dict()
        if image_size > 1024 * 1024 * 4: # > 4MB
            response["error"] = 1
            response["url"] = ""
            response["message"] = "图片不能超过4MB"
            return HttpResponse(json.dumps(response))

        md5hash = hashlib.md5(image_buffer)
        md5 = md5hash.hexdigest()

        save_path = os.path.join(BLOG_ROOT, "posts/images/" + md5 + '.' + image_name.split('.')[-1])
        print("save as %s" % save_path)

        with open(save_path, "wb") as fp:
            fp.write(image_buffer)

        if ContentImage.objects.filter(md5=md5).first():
            print("image already in database, md5=%s" % md5)
        else:
            #ContentImage(md5=md5, image=image_buffer).save()
            database = DATABASES.get("default")
            connect = pymysql.Connect(
                host=database['HOST'],
                port=int(database['PORT']),
                user=database['USER'],
                passwd=database['PASSWORD'],
                db=database['NAME'],
                charset='utf8',
            )
            sql = "insert into t_content_image (`md5`, `image`) values (%s, %s) ON DUPLICATE KEY UPDATE `image`=%s"
            cursor = connect.cursor()
            cursor.execute(sql, (md5, image_buffer, image_buffer))
            connect.commit()

        response["error"] = 0
        response["url"] = "/download_image/?md5=" + md5
        response["message"] = "上传成功"

        return HttpResponse(json.dumps(response))

def index(request):
    return render(request, 'index.html')  # 只返回页面，数据全部通过ajax获取


def set_statistic(request):
    print(request.GET)

    ip_str = request.GET.get("ip", None)
    if ip_str and isinstance(ip_str, list):
        ip_str = ip_str[0]
    else:
        try:
            ip_str = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError as err:
            print(err)
        else:
            ip_str = ip_str.split(",")[0]
            #request.META['REMOTE_ADDR'] = ip_str
    #ip_str = request.META['REMOTE_ADDR']
    print(ip_str)

    x = request.GET.get("x", '0')
    y = request.GET.get("y", '0')
    address = request.GET.get("address", "")

    province, city = '', ''

    if len(address) > 0:
        if address.endswith('市'):  # 北京市 天津市 直辖市
            province = address
            city = address
        if '自治区' in address:    # 自治区
            address = address.split('自治区')
            province = address[0]
            if len(address) > 1:
                city = address[1]
        if '省' in address:
            address = address.split('省')
            province = address[0]
            if len(address) > 1:
                city = address[1]

    if province.startswith('新疆'):
        province = '新疆'
    if province.startswith('宁夏'):
        province = '宁夏'
    if province.startswith('内蒙古'):
        province = '内蒙古'
    if province.startswith('西藏'):
        province = '西藏'
    if province.startswith('广西'):
        province = '广西'

    try:
        ip_int = socket.ntohl(struct.unpack('I',socket.inet_aton(ip_str))[0])
        SiteStatistic(ip_int=ip_int, ip_str=ip_str, province=province, city=city, x=x, y=y).save()
    except Exception as e:
        print("catch an exception when update statistic, e=%s" % e)

    response = dict()
    response["status"] = "OK"
    response["ip"] = request.META['REMOTE_ADDR']
    print(response)

    get_statistic(request)

    return HttpResponse(json.dumps(response))

def get_statistic(request):
    sql = "SELECT `x`, `y`, COUNT(*) AS count FROM `t_site_statistic` GROUP BY `x`, `y`"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    keys = [desc[0] for desc in cursor.description]
    result = []

    for r in rows:
        pos = {}
        for index, value in enumerate(r):
            pos[keys[index]] = value

        result.append(pos)

    response = dict()
    response['status'] = 'success'
    response['data'] = result

    return HttpResponse(json.dumps(response))

class StorageObject(Storage):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.file = None

    def _new_name(self, name):
        new_name = "{0}/{1}.{2}".format(self.now.strftime("%Y/%m/%d"), str(uuid.uuid4()).replace('-', ''),
                                             name.split(".").pop())
        return new_name

    def _open(self, name, mode):
        return self.file

    def _save(self, name, content):
        new_name = self._new_name(name)
        secret_id = os.environ["COS_SECRET_ID"]
        secret_key = os.environ["COS_SECRET_KEY"]
        region = 'ap-beijing'  # 替换为用户的 Region
        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)

        response = client.put_object(
            Bucket='content-image-1251916339',
            Body=content,
            Key=new_name,
            EnableMD5=False
        )
        print("upload image %s as %s to cos return %s" (name, new_name, response['ETag']))
        return "https://content-image-1251916339.cos.ap-beijing.myqcloud.com/" + name

    def exists(self, name):
        # 验证文件是否存在，因为我这边会去生成一个新的名字去存储到七牛，所以没有必要验证
        return False

    def url(self, name):
        # 上传完之后，已经返回的是全路径了
        return name

def page_not_found(request, exception):
    return render(request, '404.html')

# 500
def page_error(request):
    return render(request, '500.html')
