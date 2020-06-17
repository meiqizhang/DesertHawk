import hashlib
import json
import os
import pymysql
from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import BLOG_ROOT, DATABASES
from django.views.decorators.csrf import csrf_exempt

from apps.articles.models import ContentImage, Article
from apps.statistic.models import SiteStatistic


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


def home(request):
    if 'page_id' not in request.GET:
        visit_count = SiteStatistic.objects.filter().count()

        return render(request, 'index.html', context={"visit_count": visit_count})

    page_id = request.GET.get("page_id", "1")
    page_id = int(page_id)

    articles = Article.objects.values("title", "description", "date").order_by("click_num", "love_num")

    page_size = 7
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size

    articles = articles[from_idx: end_idx]

    context = dict()
    context["code"] = 200
    context["result"] = articles
    context['page_id'] = page_id,  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    return HttpResponse(json.dumps(context), content_type="application/json")

def page_not_found(request, exception):
    return render(request, '404.html')

# 500
def page_error(request):
    return render(request, '500.html')
