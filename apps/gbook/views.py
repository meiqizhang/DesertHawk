import json
import logging
import time

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.gbook.models import GBook
from apps.user.models import UserProfile
from apps.user.views import get_user_info_from_cookie, add_visit_history_log


@add_visit_history_log
def list(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', '')
        header = "/static/images/anonymous.jpg"
        if user_id:
            if UserProfile.objects.filter(user_id=user_id).first():
                header = UserProfile.objects.get(user_id=user_id).header
            else:
                user_id = None
        return render(request, 'templates/gbook.html', context={'user': {'id': user_id, 'header': header}})
    elif request.method == 'POST':
        response = dict()
        response["status"] = "success"
        response["msg"] = "ok"
        response["gbook"] = []

        #records = GBook.objects.filter(parent_id=-1).order_by("id").values()
        records = GBook.objects.filter().order_by("id").values()
        if records:
            for r in records:
                if r["content"].find("<img") >= 0:
                    r["content"] = r["content"].replace("<img", '<img style="width:100%"')
                response["gbook"].append(r)

        return HttpResponse(json.dumps(response), content_type="application/json")


@add_visit_history_log
def add(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "您的评论/留言成功啦~~感谢支持...^_^"

    parent_id = request.POST.get("parent", "-1")
    content = request.POST.get("content", None)

    ip_str = request.session.get("ip")
    address = request.session.get("address")
    username = request.session.get("username", None)

    logging.info("user %s add gbook from %s, ip=%s" % (username, address, ip_str))

    if not username:
        response["status"] = "error"
        response["msg"] = "登录后才能留言哟~"

        return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")

    try:
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if content is not None:
            content = content.strip()
            if len(content) > 0:
                GBook(parent_id=parent_id, user_name=username, content=content, ip=ip_str, address=address, create_time=time_now).save()
    except Exception as e:
        print("catch an exception when add msg into gbook, user_id=%s, e=%s" % (username, e))

    return HttpResponse(json.dumps(response).encode("utf-8").decode("unicode-escape"), content_type="application/json")


@add_visit_history_log
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


@add_visit_history_log
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

