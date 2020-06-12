import json
import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.comment.models import Comment
from apps.user.models import VisitUser


def commit(request):
    response = dict()

    title = request.POST.get("title")
    content = request.POST.get("content")

    ip_str = request.session.get("ip")
    address = request.session.get("address")
    user_id = request.session.get("user_id", None)

    if not user_id:
        response["status"] = "error"
        response["msg"] = "请先登录"
        return HttpResponse(json.dumps(response), content_type="application/json")

    try:
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        username = VisitUser.objects.get(id=user_id).username
        Comment.objects.create(title=title, user_name=username, content=content, ip=ip_str, address=address, create_time=time_now).save()
    except Exception as e:
        print(e)

    response["status"] = "success"
    response["msg"] = "评论成功"

    return HttpResponse(json.dumps(response), content_type="application/json")


def lists(request):
    title = request.POST.get("title", None)
    parent = request.POST.get("parent", None)

    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    if not title or not parent:
        response["status"] = "error"
        response["msg"] = "参数非法"

        return HttpResponse(json.dumps(response), content_type="application/json")

    response["comment"] = list()

    comments = Comment.objects.filter(title=title, parent_id=parent).values("id", "user_name", "address", "content", "create_time")
    for c in comments:
        response["comment"].append({"id": c["id"], "username": c["user_name"], "address": c["address"], "create_time": c["create_time"], "content": c["content"]})

    print("list comment title=%s, parent=%s, result=%d" % (title, parent, len(comments)))

    return HttpResponse(json.dumps(response), content_type="application/json")


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
