import json
import logging
import mistune
import jieba

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import JsonCustomEncoder
from apps.articles.models import Article, Tag
from apps.articles.program.stop_words import stop_words
from apps.user.models import UserProfile
from apps.user.views import add_visit_history_log


@add_visit_history_log
def home(request):
    categories = [{"name": "全部", "cat": "全部"}]

    if request.method == 'GET':
        second_category = request.GET.get("category", "全部")
        sql = "SELECT DISTINCT(second_category) FROM t_article where first_category='程序设计'"
        cursor = connection.cursor()
        cursor.execute(sql)

        for row in cursor.fetchall():
            cat = row[0]
            cat = cat.replace("+", "%2B")
            cat = cat.replace('&', "%26")
            cat = cat.replace('#', "%23")
            categories.append({"name": row[0], "cat": cat})

        return render(request, 'templates/program.html',
                      context={"categories": categories, "second_category": second_category})

    page_id = request.POST.get('page_id', '1')
    second_category = request.POST.get("category", "全部")
    logging.info("list category=%s, page id=%s" % (second_category, page_id))

    try:
        page_id = int(page_id)
    except Exception as e:
        context = dict()
        context["status"] = 'error'
        context['msg'] = '参数不对'

        return HttpResponse(json.dumps(context))

    if second_category == '全部':
        articles = Article.objects.filter(status=1, first_category="程序设计").order_by('-article_id'). \
            values("article_id", "title", "description", "date")
    else:
        articles = Article.objects.filter(first_category="程序设计", second_category=second_category, status=1). \
            order_by("-article_id").values("article_id", "title", "description", "date")

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
    context["articles"] = articles
    context['page_id'] = page_id
    context['total_pages'] = total_pages
    context['category'] = second_category
    context["page_size"] = page_size

    return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")


@add_visit_history_log
def tag(request):
    tag = request.GET.get("tag", None)

    if request.method == 'GET':
        return render(request, 'templates/tag.html', context={"tag": tag})

    tag = request.POST.get("tag", None)
    if tag:
        titles = Tag.objects.filter(tag=tag).values_list("title", flat=True)
    else:
        titles = []

    logging.info("query article with tag=%s, title=%s" % (tag, titles))

    articles = list(Article.objects.filter(title__in=titles).order_by('-date').values("title", "description", "date"))

    context = dict()
    context["status"] = 'success'
    context['msg'] = 'ok'
    context["articles"] = articles

    print(context)
    return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        return '<div><pre style="padding:0px"><code>%s</code></pre></div>' % mistune.escape(code)

    """def block_quote(self, text):  # 引用块
        html = '<blockquote style="color:gray; font-size:14px;font-style:italic">%s</blockquote>' % text
        return html """

    def image(self, src, title, alt_text):
        img = '<div style="text-align:center;"><img style="margin:auto" src="%s"></div>' % src
        return img

    def table(self, header, body):
        return '<table class="table table-bordered">\n%s\n%s</table>' % (header, body)

    """
    def paragraph(self, text):
        p = '<p>xxxxxx' + text + '</p>'
        return p
    """


@add_visit_history_log
def detail(request):
    try:
        if request.path.endswith(".html"):
            article_id = request.path.split('/')[-1].split('.')[0]
            article = Article.objects.filter(article_id=article_id, first_category="程序设计"). \
                values("article_id", "title", "date", "second_category", "description", "tags", "content", "click_num").\
                first()
            article_id = int(article_id)
        else:
            title = request.GET.get('title')
            article = Article.objects.filter(title=title, first_category="程序设计"). \
                values("article_id", "title", "date", "second_category", "description", "tags", "content", "click_num").\
                first()
            article_id = article["article_id"]
    except Exception as e:
        logging.error("catch an exception, e=%s" % e)
        article = None

    if not article:
        return render(request, "404.html")

    logging.debug("request #%d article" % article_id)

    if 'tags' in article:
        try:
            article['tags'] = eval(article['tags'])
        except Exception as e:
            try:
                article['tags'] = article['tags'].split(";")
            except Exception as e:
                article['tags'] = []

    title = article["title"]
    Article.objects.filter(article_id=article_id).update(click_num=article["click_num"] + 1)

    abouts = list()
    if 'tags' in article:
        for tag in article['tags']:
            abouts += list(Tag.objects.filter(tag=tag).values_list("title", flat=True))

    abouts = sorted(list(set(abouts)))
    while title in abouts:
        abouts.remove(title)

    abouts = list(Article.objects.filter(title__in=abouts).values("article_id", "title"))

    article_pre = Article.objects.filter(article_id__gt=article_id, first_category="程序设计") .\
        values("article_id", "title").order_by("article_id").first()
    article_next = Article.objects.filter(article_id__lt=article_id, first_category="程序设计"). \
        values("article_id", "title").order_by("-article_id").first()

    if article_pre:
        article_pre = {"article_id": article_pre["article_id"], "title": article_pre['title']}
    if article_next:
        article_next = {"article_id": article_next["article_id"], "title": article_next['title']}

    user_id = request.session.get('user_id', '')
    header = "/static/images/anonymous.jpg"

    logging.info("get user id from session=%s" % user_id)
    if user_id:
        if UserProfile.objects.filter(user_id=user_id).first():
            header = UserProfile.objects.get(user_id=user_id).header
        else:
            user_id = None

    keywords = [w for w in jieba.cut(article['content'])]
    article["keywords"] = list(set(keywords).difference(stop_words))  # b中有而a中没有的非常高效！

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    article['content'] = markdown(article['content'])

    return render(request, 'templates/detail.html', context={'article': article,
                                                             'list_about': abouts,
                                                             'article_pre': article_pre,
                                                             'article_next': article_next,
                                                             'user': {'id': user_id, 'header': header},
                                                             })
