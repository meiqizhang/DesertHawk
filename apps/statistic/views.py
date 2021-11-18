import json
import logging

import requests
from django.db.models import Count
from django.http import HttpResponse

# Create your views here.
from apps.statistic.models import SiteStatistic, IpCoordinate


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ip_address_info(ip_str):
    res = requests.get("https://api.map.baidu.com/location/ip"
                       "?ak=HQi0eHpVOLlRuIFlsTZNGlYvqLO56un3&coor=bd09ll&ip=%s" % ip_str)
    if res.status_code != 200:
        return {"code": 1}
    res_body = json.loads(res.text)
    if res_body.get("status", -1) != 0:
        logging.info("query ip %s info failed" % ip_str)
        return {"code": 1}
    content = res_body.get("content", dict())
    point = content.get("point", dict())
    address_detail = content.get("address_detail", dict())
    x = point.get("x", 0)
    y = point.get("y", 0)
    city = address_detail.get("city", "")
    province = address_detail.get("province", "")
    return {"code": 0, "x": x, "y": y, "city": city, "province": province}


def add_visit(func):
    def wrapper(request, *args, **kwargs):
        ip_str = get_client_ip(request)
        #ip_str = '183.94.105.244'
        ip_info = get_ip_address_info(ip_str)
        if ip_info["code"] != 0:
            return func(request, *args, **kwargs)

        x = ip_info["x"]
        y = ip_info["y"]
        city = ip_info["city"]
        province = ip_info["province"]

        logging.info("recv visit info, ip=%s, x=%s, y=%s, province=%s, city=%s" % (ip_str, x, y, province, city))

        coordinate = IpCoordinate.objects.filter(ip_str=ip_str).first()
        if not coordinate:
            coordinate = IpCoordinate(ip_str=ip_str, x=x, y=y, province=province, city=city)
            coordinate.save()
        else:
            last_visit_time = SiteStatistic.objects.filter(coordinate__ip_str=ip_str). \
                values("visit_time").order_by("-visit_time").first()
        SiteStatistic(url=request.path_info, coordinate=coordinate).save()
        return func(request, *args, **kwargs)
    return wrapper


def get_statistic(request):
    statistic = SiteStatistic.objects.values("coordinate__x", "coordinate__y",
                                             "coordinate__province", "coordinate__city"). \
        annotate(count=Count("coordinate__id")).all()
    for st in statistic:
        st["x"] = st["coordinate__x"]
        st["y"] = st["coordinate__y"]
        st["city"] = st["coordinate__city"]

    response = dict()
    response['status'] = 'success'
    response['data'] = list(statistic)
    return HttpResponse(json.dumps(response))
