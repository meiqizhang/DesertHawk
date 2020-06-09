import json
import time

from django.http import HttpResponse

from apps.comment.models import Comment
from apps.user.models import VisitUser


def commit(request):
    response = dict()

    user_id = request.session.get("user_id", None)
    title = request.POST.get("title")
    content = request.POST.get("content")

    ip_str = request.session.get("ip")
    address = request.session.get("address")

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
    title = request.POST.get("title")

    response = dict()
    response["status"] = "success"
    response["msg"] = "ok"

    response["comment"] = list()

    comments = Comment.objects.filter(title=title).values("user_name", "address", "content", "create_time")
    for c in comments:
        response["comment"].append({"username": c["user_name"], "address": c["address"], "create_time": c["create_time"], "content": c["content"]})

    return HttpResponse(json.dumps(response), content_type="application/json")
