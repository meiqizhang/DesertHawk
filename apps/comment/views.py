import json
import logging
import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.comment.models import Comment
from apps.statistic.views import add_visit, get_client_ip, get_ip_address_info
from apps.user.views import get_user_info_from_cookie


@add_visit
def add(request):
    response = dict()
    title = request.POST.get("title")
    content = request.POST.get("content")
    parent_id = request.POST.get("parent_id", -1)

    ip_str = get_client_ip(request)
    address_info = get_ip_address_info(ip_str)

    city = address_info.get("city", "")
    province = address_info.get("province", "")

    try:
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        Comment.objects.create(title=title, parent_id=parent_id, user_name="匿名", content=content,
                               ip=ip_str, address=province+city, create_time=time_now).save()
    except Exception as e:
        print(e)

    response["status"] = "success"
    response["msg"] = "成功啦~"

    return HttpResponse(json.dumps(response).encode('utf-8').decode("unicode-escape"), content_type="application/json")


def lists(request):
    title = request.POST.get("title", None)
    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    if not title:
        response["status"] = "error"
        response["msg"] = "参数非法"

        return HttpResponse(json.dumps(response), content_type="application/json")

    response["comments"] = list()

    comments = Comment.objects.filter(title=title, status='p').values()
    for c in comments:
        response["comments"].append(c)

    logging.info("list comment title=%s, result=%d" % (title, len(comments)))

    return HttpResponse(json.dumps(response), content_type="application/json")


@add_visit
def reply(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    user_id = request.session.get("user_id", None)
    title = request.POST.get("title")
    parent_id = request.POST.get("parent")
    content = request.POST.get("content")
    current_url = request.POST.get("current_url")
    ip_str = request.session.get("ip")
    address = request.session.get("address")

    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    print(title, parent_id, content, current_url)
    username='zhangqi'
    Comment.objects.create(title=title, parent_id=parent_id, user_name=username, content=content, ip=ip_str, address=address,
                           create_time=time_now).save()

    if title or len(title) > 0:
       return redirect(current_url)

    return HttpResponse(json.dumps(response), content_type="application/json")


@add_visit
def ding(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    user = get_user_info_from_cookie(request)
    id = request.POST.get("id", None)

    logging.info("user %s ip=%s, address=%s ding the comment [%s]" % (user["username"], user["ip"], user["address"], id))

    gbook = Comment.objects.filter(id=id).values("ding").first()
    if gbook:
        Comment.objects.filter(id=id).update(ding=gbook["ding"] + 1)
    else:
        logging.error("the %s comment not exist" % id)
        response["status"] = "error"
        response["msg"] = "是不是点错了~"
        return HttpResponse(json.dumps(response), content_type="application/json")

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

    logging.info("user %s ip=%s, address=%s cai the comment [%s]" % (user["username"], user["ip"], user["address"], id))

    gbook = Comment.objects.filter(id=id).values("cai").first()
    if gbook:
        Comment.objects.filter(id=id).update(cai=gbook["cai"] + 1)
    else:
        logging.error("the %s comment not exist" % id)
        response["status"] = "error"
        response["msg"] = "是不是点错了~"
        return HttpResponse(json.dumps(response), content_type="application/json")

    response["data"] = dict()
    response["data"]["cai"] = gbook["cai"] + 1
    return HttpResponse(json.dumps(response), content_type="application/json")


def comment_html(request):
    return render(request, 'templates/comment.html', context={})
