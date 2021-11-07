import json

from django.http import HttpResponse

# Create your views here.
from apps.linking.models import Linking


def list_links(request):
    links = Linking.objects.filter(status=1).values().all()
    links = list(links)
    response = {"code": 0, "links": links}
    return HttpResponse(json.dumps(response), content_type="application/json")

