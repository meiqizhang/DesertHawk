from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.articles.models import Article


def search(request):
    # SELECT title, MATCH (title) AGAINST ('矩阵分解') AS score FROM t_article_index WHERE MATCH (title) AGAINST ('矩阵分解' IN NATURAL LANGUAGE MODE);
    keyword = request.GET.get("keyword", None)

    if keyword:
        sql = "select DISTINCT(title), MATCH (content) AGAINST ('%s') AS score FROM t_article_index WHERE MATCH (content) AGAINST ('%s' IN NATURAL LANGUAGE MODE)" % (keyword, keyword)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = list()
            for row in cursor.fetchall():
                title, score = row[0], row[1]
                article = Article.objects.filter(title=title).first()

                #.date.strftime('%Y-%m-%d %H:%I:%S')
                results.append({"title": title, "score": score, "description": article.description, "date": article.date.strftime('%Y-%m-%d %H:%I:%S')})

            print(results)
    else:
        results = list()

    return render(request, 'search.html', context={"articles": results, "keyword": keyword})

