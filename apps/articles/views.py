import json
import logging

import jieba
import mistune
from django import db
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from DesertHawk.settings import cos_client, JsonCustomEncoder
from apps.articles.models import Article, Tag
from apps.articles.stop_words import stop_words
from apps.user.models import UserProfile
from apps.user.views import add_visit_history_log


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
    title = request.POST.get("title", None)
    if not title:
        id = request.POST.get("id", None)
        if id:
            title = Article.objects.get(id=id).title

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

    imgtype = file.name.split('.')[-1]
    ret = cos_client.put_object(
        Bucket='article-surface-1251916339',
        Body=image,
        Key="%s.%s" % (title, imgtype),
        EnableMD5=False
    )
    return HttpResponse(json.dumps(response), content_type="application/json")


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        return '<div><pre style="padding:0px; background: #f0f0f0;" class="prettyprint linenums:1">%s</pre></div>' % mistune.escape(
            code)

    """def block_quote(self, text):  # 引用块
        html = '<blockquote style="color:gray; font-size:14px;font-style:italic">%s</blockquote>' % text
        return html """

    def codespan(self, text):
        return '<code style="color: #0000ff; font-weight:bold">' + text + '</code>'

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
    article_id = int(request.path.split('/')[-1].split('.')[0])
    article = Article.objects.filter(article_id=article_id).values().first()
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

    Article.objects.filter(article_id=article_id).update(click_num=article["click_num"] + 1)

    abouts = list()
    if 'tags' in article:
        for tag in article['tags']:
            abouts += list(Tag.objects.filter(tag=tag).values_list("title", flat=True))

    self_tile = article["title"]
    abouts = sorted(list(set(abouts)))
    while self_tile in abouts:
        abouts.remove(self_tile)

    abouts = list(Article.objects.filter(title__in=abouts).values("article_id", "title"))

    article_pre = Article.objects.filter(article_id__gt=article_id).values("article_id", "title").order_by(
        "article_id").first()
    article_next = Article.objects.filter(article_id__lt=article_id).values("article_id", "title").order_by(
        "-article_id").first()

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
    context = {'article': article, 'list_about': abouts, 'article_pre': article_pre,
               'article_next': article_next, 'user': {'id': user_id, 'header': header}
               }
    return render(request, 'detail.html', context=context)


@add_visit_history_log
def tag(request):
    req_tag = request.path.split('/')[-1]
    titles = Tag.objects.filter(tag=req_tag).values_list("title", flat=True)

    logging.info("query article with tag=%s, title=%s" % (req_tag, titles))

    articles = list(Article.objects.filter(title__in=titles).order_by('-date').values())
    for article in articles:
        article["year"] = article["date"].strftime('%Y')
        article["day"] = article["date"].strftime('%m-%d')
    context = dict()
    context["tag"] = req_tag
    context["status"] = 'success'
    context['msg'] = 'ok'
    context["articles"] = articles
    return render(request, "tag.html", context=context)


@add_visit_history_log
def programing(request):
    category = request.GET.get("category", None)
    articles = Article.objects.filter(status=1, first_category='程序设计').order_by("-article_id").\
        values("article_id", "title", "second_category", "description", "date")

    categories = set()
    for article in articles:
        categories.add(article['second_category'])
        article["description"] = article["description"][:70]
        article["year"] = article["date"].strftime('%Y')
        article["day"] = article["date"].strftime('%m-%d')

    context = dict()
    context["code"] = 200
    context["categories"] = list(categories)
    context["category"] = category if category is not None else "程序设计"
    if category is None:
        context["articles"] = articles
    else:
        context["articles"] = [x for x in articles if x["second_category"] == category]
    return render(request, "programing.html",context=context)
