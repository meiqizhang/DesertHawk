import json

import markdown2
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from DesertHawk.settings import JsonCustomEncoder
from apps.articles.models import Article, Tag
from apps.user.models import UserProfile
from apps.user.views import get_user_info_from_cookie


def home(request):
    page_id = request.GET.get('page_id', '1')
    second_category = request.GET.get("category", '')

    if len(second_category) == 0:
        sql = "SELECT DISTINCT(second_category) FROM t_article where first_category='程序设计'"
        cursor = connection.cursor()
        cursor.execute(sql)
        categories = ["全部"]

        for row in cursor.fetchall():
            categories.append(row[0])

        return render(request, 'templates/program.html', context={"categories": categories})

    try:
        page_id = int(page_id)
    except Exception as e:
        context = dict()
        context["status"] = 'error'
        context['msg'] = '参数不对'

        return HttpResponse(json.dumps(context))

    if second_category == '全部':
        articles = Article.objects.all().order_by('-date').values("title", "description", "date")
    else:
        articles = Article.objects.filter(first_category="程序设计",second_category=second_category).order_by("-click_num").order_by('-date').values("title", "description", "date")

    page_size = 7
    total_pages = int(len(articles) / page_size)
    if len(articles) % page_size != 0:
        total_pages += 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size

    articles = articles[from_idx: end_idx]

    context = dict()
    context["status"] = 'success'
    context['msg'] = 'ok'
    context["result"] = articles
    context['page_id'] = page_id
    context['total_pages'] = total_pages
    context['category'] = second_category
    context["page_size"] = page_size

    # print("request No.%d page, return %d articles" % (page_id, len(articles)))
    if not second_category or len(second_category) < 1:
        return render(request, 'learn.html', context={'articles': articles})
    else:
        return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

def detail(request):
    title = request.GET.get('title')
    article = Article.objects.filter(title=title, first_category="程序设计").values("id", "title", "date", "second_category", "description", "tags", "content", "click_num").first()

    if not article:
        return render(request, "404.html")

    if 'tags' in article:
        try:
            article['tags'] = eval(article['tags'])
        except Exception as e:
            article['tags'] = []

    Article.objects.filter(title=title).update(click_num=article["click_num"] + 1)

    abouts = list()
    if 'tags' in article:
        for tag in article['tags']:
            abouts += list(Tag.objects.filter(tag=tag).values_list("title", flat=True))

    abouts = sorted(list(set(abouts)))
    if title in abouts:
        abouts.remove(title)

    id = article['id']
    article_pre = Article.objects.filter(id__lt=id).values("title").order_by("-id").first()
    article_next = Article.objects.filter(id__gt=id).values("title").order_by("id").first()

    if article_pre:
        article_pre = article_pre['title']
    if article_next:
        article_next = article_next['title']

    user_id = request.session.get('user_id', '')
    header = "/static/images/anonymous.jpg"

    print("get user id from sessoion=%s" % user_id)
    if user_id:
        if UserProfile.objects.filter(user_id=user_id).first():
            header = UserProfile.objects.get(user_id=user_id).header
        else:
            user_id = None

    user = get_user_info_from_cookie(request)

    #article['content'] = markdown2.markdown(article['content'].replace("\r\n", '  \n'),
    #                                        extras=["code-friendly"])

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    article['content'] = mistune.markdown(article['content'])

    return render(request, 'templates/detail.html', context={'article': article,
                                                    'list_about': abouts,
                                                    'article_pre': article_pre,
                                                    'article_next': article_next,
                                                    'user': {'id': user_id, 'header': header}
                                                    })


