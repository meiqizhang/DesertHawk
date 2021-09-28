from apps.statistic.models import SiteStatistic
from . import settings


def theme(request):
    return {'THEME': settings.THEME}


def visit_count(request):
    return {"VISIT_COUNT": SiteStatistic.objects.filter().count()}