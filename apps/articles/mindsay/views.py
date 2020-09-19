import logging

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.articles.models import Article


def home(request):
    articles = list(Article.objects.filter(first_category="mindsay").values("article_id", "title", "date", "description", "content"))

    context = {"articles": list()}
    for article in articles:
        context["articles"].append({"article_id": article["article_id"],
                                    "title": article["title"],
                                    "description": article["description"],
                                    "date": article["date"].strftime('%Y-%m-%d %H:%M:%S'),
                                    "content": article["content"]})

    return render(request, 'articles/mindsay/templates/index.html', context=context)


def detail(request):
    try:
        article_id = request.path.split('/')[-1].split('.')[0]
    except Exception as e:
        logging.error("catch an exception, e=%s" % e)
        return render(request, "404.html")

    article = Article.objects.filter(article_id=article_id).values("article_id", "title", "date", "description", "content").first()

    date = article["date"].strftime('%Y-%m-%d').split('-')
    year, month, day = date[:3]

    article = {"article_id": article["article_id"],
               "title": article["title"],
               "description": article["description"],
               "date": "%s年%s月%s日" % (year, month, day),
               "content": article["content"]}

    return render(request, 'articles/mindsay/templates/detail.html', context={"article": article})
