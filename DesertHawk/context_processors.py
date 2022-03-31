import time
import datetime
from apps.statistic.models import SiteStatistic
from . import settings


def theme(request):
    return {'THEME': settings.THEME}


def visit_count(request):
    statistic = SiteStatistic.objects.values("coordinate_id", "visit_time", "coordinate__x", "coordinate__y",
                                             "coordinate__province", "coordinate__city")
    # 连续一小时内的同一个IP算一次访问
    result = list()
    last_time = None
    last_coordinate_id = None
    for st in statistic:
        visit_date = datetime.datetime.strptime(str(st["visit_time"])[:19], "%Y-%m-%d %H:%M:%S")
        visit_time = time.mktime(visit_date.timetuple())

        if last_time is not None:
            if st["coordinate_id"] == last_coordinate_id and visit_time - last_time < 3600:
                continue
            else:
                result.append(st)
                last_time = visit_time
                last_coordinate_id = st["coordinate_id"]
        else:
            result.append(st)
            last_time = visit_time
            last_coordinate_id = st["coordinate_id"]
    return {"VISIT_COUNT": len(result)}
    # return {"VISIT_COUNT": SiteStatistic.objects.filter().count()}

