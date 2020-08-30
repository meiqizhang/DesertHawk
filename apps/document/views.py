from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.document.models import Document


def list(request):
    """    file = open('static/files/BatchPayTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="BatchPayTemplate.xls"'
    return response"""

    documents = []
    for doc in Document.objects.all():
        documents.append({"name": doc.name, "url": doc.url, "download_count": doc.download_count, "date": doc.create_time.strftime('%Y-%m-%d %H:%I:%S')})

    print(documents)

    return render(request, 'document/templates/document.html', context={"documents": documents})
