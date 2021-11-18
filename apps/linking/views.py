import json

from django.http import HttpResponse

# Create your views here.
from apps.linking.models import Linking


def list_links(request):
    links = Linking.objects.filter(status=1).values("id", "name", "href", "title").all()
    links = list(links)
    response = {"code": 0, "links": links}
    return HttpResponse(json.dumps(response), content_type="application/json")


def click_links(request):
    link_id = request.GET.get("id")
    link = Linking.objects.get(id=link_id)
    link.click_num = link.click_num + 1
    link.save()
    return HttpResponse(json.dumps({"code": "success"}), content_type="application/json")

