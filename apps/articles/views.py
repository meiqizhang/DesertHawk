import json
import logging
import time

from django import db
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DesertHawk.settings import cos_client
from apps.articles.models import Article



@csrf_exempt
def download_icon(request):
    if 'title' in request.GET:
        title = request.GET.get('title', '')
    else:
        title = request.POST.get('title', '')

    response = dict()

    record = Article.objects.raw("select id, image from t_article where title=%s", [title])
    if len(record) > 0:
        record = record[0]
        image = record.image

        response["status"] = "success"
        response["image"] = image
    else:
        response["status"] = "error"

    return HttpResponse(response["image"])


@csrf_exempt
def upload_icon(request):

    title = request.POST.get("title")
    file = request.FILES.get('file')
    image = file.read()
    response = dict()

    try:
        with db.connection.cursor() as cur:
            ret = cur.execute("update t_article set image=%s where title=%s", [image, title])
            logging.info("update '%s' image return %s" % (title, ret))
            response["status"] = "success"
            response["msg"] = "成功"
    except Exception as e:
        response["status"] = "error"
        response["msg"] = str(e)
        logging.error("update article image failed, title=%s, e=%s" % (title, e))

    """
    imgtype = file.name.split('.')[-1]
    response = cos_client.put_object(
            Bucket='article-surface-1251916339',
            Body=image,
            Key="%s.%s" % (title, imgtype),
            EnableMD5=False
        )

    try:
        print(file.name)
        url = "https://article-surface-1251916339.cos.ap-beijing.myqcloud.com/%s.%s" % (title, imgtype)
        print(url)

        with db.connection.cursor() as cur:
            ret = cur.execute("update t_article set image=%s where title=%s", [url, title])
            logging.info("update '%s' image return %s" % (title, ret))
            response["status"] = "success"
            response["msg"] = "成功"
    except Exception as e:
        response["status"] = "error"
        response["msg"] = str(e)
        logging.error("update article image failed, title=%s, e=%s" % (title, e))
    """
    return HttpResponse(json.dumps(response), content_type="application/json")

