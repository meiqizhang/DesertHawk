import json

from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import JsonCustomEncoder
from apps.articles.models import ContentImage, Article
from apps.home.fetch_news import fetch_toutiao_news
from apps.user.views import add_visit_history_log


@add_visit_history_log
def home(request):
    articles = Article.objects.filter(status=1).order_by("-article_id").values("article_id", "title", "first_category", "description", "date")
    page_id = request.GET.get("page_id", "1")
    width = int(request.GET.get("width", "0"))

    page_id = int(page_id)
    page_size = 7
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size
    articles = articles[from_idx: end_idx]

    for article in articles:
        article["description"] = article["description"][:70]
        article["year"] = article["date"].strftime('%Y')
        article["day"] = article["date"].strftime('%m-%d')
        article["url"] = "/articles/program/detail/"
        if article["first_category"] == "mindsay":
            article["url"] = "/articles/mindsay/detail/"

    context = dict()
    context["code"] = 200
    context["figure_articles"] = articles[:3]
    context["articles"] = articles[3:]
    context['page_id'] = page_id  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    if 'page_id' in request.GET:
        return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")
    else:
        print("width", width)
        return render(request, "index.html",context=context)  # 只返回页面，数据全部通过ajax获取


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


@add_visit_history_log
def homexx(request):
    return index(request)

    if 'page_id' not in request.GET:
        return render(request, 'index.html')

    page_id = request.GET.get("page_id", "1")
    page_id = int(page_id)

    articles = Article.objects.filter(status=1).order_by("-article_id").values("article_id", "title", "first_category", "description", "date")

    page_size = 7
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size

    articles = articles[from_idx: end_idx]

    for article in articles:
        article["description"] = article["description"][:70]

    context = dict()
    context["code"] = 200
    context["result"] = articles
    context['page_id'] = page_id,  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")


def page_not_found(request, exception):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')

def fetch_news(request):
    max_behot_time = '0'  # 链接参数
    title = []  # 存储新闻标题
    source_url = []  # 存储新闻的链接
    s_url = []  # 存储新闻的完整链接
    source = []  # 存储发布新闻的公众号
    media_url = {}  # 存储公众号的完整链接
    ip_str = request.COOKIES.get("ip")
    if ip_str is None or len(ip_str) < 7:
        print("ignore fetch news request, ip_str=", ip_str)
        return HttpResponse(json.dumps({"code": 0, "news": []}), content_type="application/json")

    result = fetch_toutiao_news(max_behot_time, title, source_url, s_url, source, media_url)
    return HttpResponse(json.dumps({"code": 0, "news": result}, ensure_ascii=False),  content_type="application/json")
