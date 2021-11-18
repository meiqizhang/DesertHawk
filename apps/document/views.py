import logging

from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.document.models import Document
from apps.statistic.views import add_visit


@add_visit
def list(request):
    documents = []
    for doc in Document.objects.all().order_by("name"):
        documents.append({"name": doc.name, "url": doc.url, "download_count": doc.download_count, "date": doc.create_time.strftime('%Y-%m-%d %H:%I:%S')})

    return render(request, 'document/templates/document.html', context={"documents": documents})


@add_visit
def download(request):
    logging.info("download request=%s" % request.body)
    name = request.GET.get("name", None)

    if not name:
        return HttpResponse("error, name is None")

    doc = Document.objects.get(name=name)
    doc.download_count = doc.download_count + 1
    doc.save()
    return HttpResponse("success")
