import json

from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import JsonCustomEncoder
from apps.articles.models import ContentImage, Article
from apps.user.views import add_visit_history_log


@add_visit_history_log
def home(request):
    articles = Article.objects.filter(status=1).order_by("-article_id").values("article_id", "title", "first_category", "description", "date")
    page_id = request.GET.get("page_id", "1")

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

    context = dict()
    context["code"] = 200
    context["figure_articles"] = articles[:3]
    context["articles"] = articles[3:]
    context['page_id'] = page_id  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    if 'page_id' in request.GET:
        return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")
    else:
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
