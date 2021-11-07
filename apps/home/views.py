import json

from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import JsonCustomEncoder
from apps.articles.models import Article
from apps.statistic.views import add_visit
from apps.user.views import add_visit_history_log


@add_visit
def home(request):
    articles = Article.objects.filter(status='p').order_by("-article_id").values("article_id", "title", "cover__pic", "abstract", "date")
    page_id = request.GET.get("page", "1")

    page_id = int(page_id)
    page_size = 7
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size
    articles = articles[from_idx: end_idx]

    for article in articles:
        article["cover_pic"] = article["cover__pic"]
        article["abstract"] = article["abstract"][:70]
        article["year"] = article["date"].strftime('%Y')
        article["day"] = article["date"].strftime('%m-%d')

    context = dict()
    context["code"] = 200
    context["figure_articles"] = articles[:3]
    context["articles"] = articles[3:]
    context['page'] = page_id  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    # if 'page_id' in request.GET:
    #     return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")
    # else:
    #     return render(request, "index.html",context=context)
    return render(request, "index.html",context=context)


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


def page_not_found(request, exception):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')
