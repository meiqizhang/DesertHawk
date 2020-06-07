import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.articles.models import Article


def upload_icon(request):
    print(request)

@csrf_exempt
def download_icon(request):
    if 'title' in request.GET:
        title = request.GET.get('title', '')
    else:
        title = request.POST.get('title', '')

    print("get article image, title=%s" % title)
    response = dict()

    record = Article.objects.filter(title=title).values("image").first()
    if record:
        image = record['image']
        if len(image) < 256: # 图片的URL
            with open(image, 'rb') as fp:
                image = fp.read()

        response["status"] = "success"
        response["image"] = image
    else:
        response["status"] = "error"

    return HttpResponse(response["image"])



