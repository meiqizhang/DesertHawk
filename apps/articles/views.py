import json
import logging

import mistune
import markdown
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.articles.models import Article, Tag, Cover, Category
from apps.statistic.views import add_visit


@csrf_exempt
def update_cover_pic(request):
    # file = request.FILES.get('file')
    # pic_buf = file.read()
    # Cover(pic_buf=pic_buf).save()
    # return HttpResponse(json.dumps({"code": 0}), content_type="application/json")
    logging.info(request.body)
    req_body = json.loads(request.body)
    cover_id = req_body["cover_id"]
    article_id = req_body["article_id"]
    logging.info("update article %d cover to %d" % (article_id, cover_id))
    Article.objects.filter(article_id=article_id).update(cover=cover_id)
    response = {"code": 0, "msg": "success"}
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


class CommonMarkdown:
    @staticmethod
    def _convert_markdown(value):
        md = markdown.Markdown(
            extensions=[
                'extra',
                'codehilite',
                'toc',
                'tables',
            ]
        )
        body = md.convert(value)
        toc = md.toc
        return body, toc

    @staticmethod
    def get_markdown_with_toc(value):
        body, toc = CommonMarkdown._convert_markdown(value)
        return body, toc

    @staticmethod
    def get_markdown(value):
        body, toc = CommonMarkdown._convert_markdown(value)
        return body, toc


@add_visit
def detail(request):
    article_id = int(request.path.split('/')[-1].split('.')[0])
    article_obj = Article.objects.get(article_id=article_id)
    if not article_obj:
        return render(request, "404.html")
    logging.debug("request #%d article" % article_id)

    article_obj.click_num = article_obj.click_num + 1
    article_obj.save()
    tag_list = ["%s" % tag for tag in article_obj.tags.all()]
    article = dict()
    article["article_id"] = article_obj.article_id
    article["title"] = article_obj.title
    article["second_category"] = article_obj.category
    article["first_category"] = article_obj.category.parent.name
    article["tags"] = tag_list
    article["abstract"] = article_obj.abstract
    article["content"] = article_obj.content
    article["date"] = article_obj.date
    article["click_num"] = article_obj.click_num
    article["love_num"] = article_obj.love_num
    article["cover"] = article_obj.cover

    abouts_article = list(Article.objects.filter(tags__name__in=tag_list).values("article_id", "title").
                          exclude(article_id=article_obj.article_id))
    abouts_id = set()
    abouts = list()
    for blog in abouts_article:
        article_id = blog["article_id"]
        if article_id not in abouts_id:
            abouts.append(blog)
            abouts_id.add(article_id)

    article_pre = Article.objects.filter(article_id__gt=article_id).values("article_id", "title").order_by(
        "article_id").first()
    article_next = Article.objects.filter(article_id__lt=article_id).values("article_id", "title").order_by(
        "-article_id").first()

    if article_pre:
        article_pre = {"article_id": article_pre["article_id"], "title": article_pre['title']}
    if article_next:
        article_next = {"article_id": article_next["article_id"], "title": article_next['title']}

    content = article['content'].replace("\r\n", ' \n')
    old = content
    while True:
        new = old.replace(" ```", "```")
        if new == old:
            break
        old = new
    content = old
    article['content'], article["toc"] = CommonMarkdown.get_markdown(content)
    context = {
        'article': article,
        'list_about': abouts,
        'article_pre': article_pre,
        'article_next': article_next,
    }
    return render(request, 'detail.html', context=context)


@add_visit
def programing(request):
    category = request.GET.get("category", None)
    tag = request.GET.get("tag", None)
    page_id = request.GET.get("page", "1")
    categories = list(Category.objects.filter(parent__name='程序设计').values_list("name", flat=True))

    if tag is None:
        if category is None:
            category = "程序设计"
            articles = Article.objects.filter(status='p', category__parent__name=category).order_by("-article_id"). \
                values("article_id", "title", "abstract", "tags__name", "date", "category__name", "cover__pic").distinct()
        else:
            articles = Article.objects.filter(status='p', category__name=category).order_by("-article_id"). \
                values("article_id", "title", "abstract", "tags__name", "date", "category__name", "cover__pic")
    else:
        articles = Article.objects.filter(status='p', tags__name=tag).order_by("-article_id"). \
            values("article_id", "title", "abstract", "tags", "date", "category", "cover__pic")

    articles_id_set = set(x["article_id"] for x in articles)
    tmp_articles = list()
    for article in articles:
        if article["article_id"] in articles_id_set:
            tmp_articles.append(article)
            articles_id_set.remove(article["article_id"])
    articles = tmp_articles

    for article in articles:
        article["abstract"] = article["abstract"][:70]
        article["cover_url"] = article["cover__pic"]
        article["year"] = article["date"].strftime('%Y')
        article["day"] = article["date"].strftime('%m-%d')

    context = dict()
    context["code"] = 200
    context["categories"] = categories
    context["category"] = category

    page_id = int(page_id)
    page_size = 10
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = from_idx + page_size
    articles = articles[from_idx: end_idx]

    context["page"] = page_id
    context["total_pages"] = total_pages
    context["category"] = category
    context["articles"] = articles
    print(articles)

    return render(request, "programing.html", context=context)
