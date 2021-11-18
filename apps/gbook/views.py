import json
import logging
import time


from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.gbook.models import GBook
from apps.statistic.views import add_visit, get_client_ip, get_ip_address_info
from apps.user.views import get_user_info_from_cookie


@add_visit
def list(request):
    if request.method == 'GET':
        return render(request, 'templates/gbook.html')
    elif request.method == 'POST':
        response = dict()
        response["status"] = "success"
        response["msg"] = "ok"
        response["gbook"] = []

        records = GBook.objects.filter().order_by("id").values()
        if records:
            for r in records:
                r["create_time"] = r["create_time"].strftime('%Y-%m-%d %H:%M')
                if r["content"].find("<img") >= 0:
                    r["content"] = r["content"].replace("<img", '<img class="gbook-img"')
                response["gbook"].append(r)

        return HttpResponse(json.dumps(response), content_type="application/json")


@add_visit
def add(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "您的评论/留言成功啦~~感谢支持...^_^"

    parent_id = request.POST.get("parent", "-1")
    content = request.POST.get("content", None)

    ip_str = get_client_ip(request)
    address_info = get_ip_address_info(ip_str)

    city = address_info.get("city", "")
    province = address_info.get("province", "")

    try:
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if content is not None:
            content = content.strip()
            if len(content) > 0:
                GBook(parent_id=parent_id, user_name="", content=content, ip=ip_str, address=province+city, create_time=time_now).save()
    except Exception as e:
        print("catch an exception when add msg into gbook, e=%s" % e)

    return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")


@add_visit
def ding(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    user = get_user_info_from_cookie(request)
    id = request.POST.get("id", None)

    logging.info("user %s ip=%s, address=%s ding the gbook [%s]" % (user["username"], user["ip"], user["address"], id))

    gbook = GBook.objects.filter(id=id).values("ding").first()
    if gbook:
        GBook.objects.filter(id=id).update(ding=gbook["ding"] + 1)
    else:
        logging.error("the %s gbook not exist" % id)
        response["status"] = "error"
        response["msg"] = "是不是点错了~"
        return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")

    response["data"] = dict()
    response["data"]["ding"] = gbook["ding"] + 1
    return HttpResponse(json.dumps(response), content_type="application/json")


@add_visit
def cai(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    user = get_user_info_from_cookie(request)
    id = request.POST.get("id", None)

    logging.info("user %s ip=%s, address=%s cai the gbook [%s]" % (user["username"], user["ip"], user["address"], id))

    gbook = GBook.objects.filter(id=id).values("cai").first()
    if gbook:
        GBook.objects.filter(id=id).update(cai=gbook["cai"] + 1)
    else:
        logging.error("the %s gbook not exist" % id)
        response["status"] = "error"
        response["msg"] = "是不是点错了~"
        return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")

    response["data"] = dict()
    response["data"]["cai"] = gbook["cai"] + 1
    return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")

