import logging

import mistune
from django.shortcuts import render

# Create your views here.
from apps.articles.models import Article
from apps.articles.program.views import HighlightRenderer
from apps.user.models import UserProfile
from apps.user.views import add_visit_history_log


@add_visit_history_log
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


@add_visit_history_log
def detail(request):
    try:
        article_id = request.path.split('/')[-1].split('.')[0]
    except Exception as e:
        logging.error("catch an exception, e=%s" % e)
        return render(request, "404.html")

    article = Article.objects.filter(article_id=article_id).values("article_id", "title", "date", "description", "content").first()

    date = article["date"].strftime('%Y-%m-%d').split('-')
    year, month, day = date[:3]

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    article['content'] = markdown(article['content'])

    user_id = request.session.get('user_id', '')
    header = "/static/images/anonymous.jpg"

    if user_id:
        if UserProfile.objects.filter(user_id=user_id).first():
            header = UserProfile.objects.get(user_id=user_id).header
        else:
            user_id = None

    article = {"article_id": article["article_id"],
               "title": article["title"],
               "description": article["description"],
               "date": "%s年%s月%s日" % (year, month, day),
               "content": article["content"]}

    return render(request, 'articles/mindsay/templates/detail.html', context={"article": article, 'user': {'id': user_id, 'header': header}})
