import json
import logging
import socket
import struct
import time

from django.db import connection
from django.http import HttpResponse

# Create your views here.
from apps.statistic.models import SiteStatistic, CityCoordinate


def set_statistic(request):
    ip_str = request.GET.get("ip", None)
    x = request.GET.get("x", '0')
    y = request.GET.get("y", '0')
    address = request.GET.get("address", "")

    logging.info("recv visit info, ip=%s, x=%s, y=%s, address=%s" % (ip_str, x, y, address))

    province, city = '', ''

    if len(address) > 0:
        if address.endswith('市'):  # 北京市 天津市 直辖市
            province = address
            city = address
        if '自治区' in address:    # 自治区
            address = address.split('自治区')
            province = address[0] + "自治区"
            if len(address) > 1:
                city = address[1]
        if '省' in address:
            address = address.split('省')
            province = address[0] + "省"
            if len(address) > 1:
                city = address[1]

    if province.startswith('新疆'):
        province = '新疆'
    if province.startswith('宁夏'):
        province = '宁夏'
    if province.startswith('内蒙古'):
        province = '内蒙古'
    if province.startswith('西藏'):
        province = '西藏'
    if province.startswith('广西'):
        province = '广西'

    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    try:
        ip_int = socket.ntohl(struct.unpack('I',socket.inet_aton(ip_str))[0])
        SiteStatistic(ip_int=ip_int, ip_str=ip_str, province=province, city=city, x=x, y=y, visit_time=time_now).save()

        row = CityCoordinate.objects.filter(x=x, y=y).first()
        logging.info(row)
        #logging.info(len(row))

        if CityCoordinate.objects.filter(x=x, y=y).first():
            if len(province) > 0:
                CityCoordinate.objects.filter(x=x, y=y).update(province=province)
            if len(city) > 0:
                CityCoordinate.objects.filter(x=x, y=y).update(city=city)
        else:
            CityCoordinate(province=province, city=city, x=x, y=y).save()
            logging.info("add city coordinate, x=%s, y=%s, city=%s, province=%s" % (x, y, city, province))
    except Exception as e:
        logging.error("catch an exception when update statistic, e=%s" % e)

    response = dict()
    response["status"] = "OK"

    return HttpResponse(json.dumps(response))


def get_statistic(request):
    sql = "SELECT `x`, `y`, COUNT(*) AS count FROM `t_site_statistic` GROUP BY `x`, `y`"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    keys = [desc[0] for desc in cursor.description]
    result = []

    for r in rows:
        pos = {}
        for index, value in enumerate(r):
            pos[keys[index]] = value

        if 'x' in pos and 'y' in pos:
            x = pos['x']
            y = pos['y']
            try:
                record = CityCoordinate.objects.get(x=x, y=y)
                pos["city"] = record.city
            except Exception as e:
                logging.error("catch an exception, e=%s" % e)
                pos["city"] = "未知"

        result.append(pos)

    response = dict()
    response['status'] = 'success'
    response['data'] = result

    return HttpResponse(json.dumps(response))
