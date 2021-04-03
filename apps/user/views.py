#encoding=utf-8

import json
import urllib
import time
import random
from urllib.parse import urlencode

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from DesertHawk.settings import sms_app_id, sms_app_key
from apps.user.models import UserProfile, SMSStatus, VisitHistory
from qcloudsms_py import SmsSingleSender


def add_visit_history_log(func):
    def wrapper(request, *args, **kwargs):
        ip_str = request.COOKIES.get("ip")
        params = '&'
        for p in request.GET:
            params += p + '=' + request.GET.get(p)

        if len(params) > 1:
            VisitHistory(ip_str=ip_str, url=request.path + "?" + params[1:]).save()
        else:
            VisitHistory(ip_str=ip_str, url=request.path).save()

        return func(request, *args, **kwargs)

    return wrapper


def get_user_info_from_cookie(request):
    user = dict()
    user["username"] = request.COOKIES.get("username")
    user["ip"] = request.COOKIES.get("ip")
    user["address"] = request.COOKIES.get("address")

    return user


@add_visit_history_log
def login(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "成功"
    response["user"] = dict()

    if request.method == 'GET':
        return render(request, 'login.html')

    login_type = request.POST.get("login_type", None)
    print("login type=%s" % login_type)

    response = dict()
    if login_type == "username":
        response = login_with_user_name(request)
    elif login_type == "sms":
        response = login_with_sms_code(request)

    if response and response["status"] == "success":
        request.session["ip"] = request.POST.get("ip")
        request.session["address"] = request.POST.get("address")
        print("login success, save ip and address into session..., ip=%s, address=%s" % (request.session["ip"], request.session["address"]))

    return HttpResponse(json.dumps(response), content_type="application/json")


# 用户注册
@add_visit_history_log
def regist(request):
    if request.method == 'GET':
        return render(request, 'templates/register.html')

    if request.method == "POST":
        response = dict()

        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        sms_code = request.POST.get("sms_code")

        sms_status = SMSStatus.objects.filter(phone=phone_number, code=sms_code).values("create_time").first()
        if sms_status:
            pass
        else:
            response["status"] = "error"
            response["msg"] = "验证码错误~"
            return HttpResponse(json.dumps(response).encode('utf-8').decode("unicode-escape"),
                                content_type="application/json")

        users = UserProfile.objects.filter(Q(user__username=username) | Q(phone=phone_number)).exists()
        if users:
            response["status"] = "error"
            response["msg"] = "该用户名或手机号已经被注册了，换个试试吧~"
            return HttpResponse(json.dumps(response).encode('utf-8').decode("unicode-escape"),
                                content_type="application/json")
        else:
            User.objects.create(username=username, password=make_password(password))

            print(password, make_password(password))

            user = UserProfile()
            user.user_id = User.objects.get(username=username).id
            user.phone = phone_number
            user.header = "https://user-header-1251916339.cos.ap-beijing.myqcloud.com/default.jpg"
            user.save()
            response["status"] = "success"
            response["msg"] = "注册成功啦，返回原页面登录就可以啦~"
            return HttpResponse(json.dumps(response).encode('utf-8').decode('unicode_escape'), content_type="application/json")

#注销账户
def user_logout(request):
    # request.session.flush()  #删除了Cookie session 缓存里的信息

    #调用函数
    logout(request)
    return redirect(reverse('index'))


def get_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def util_sendmsg(mobile, check_code):
    #APPID = '1400391229'
    #APPKEY = '24a1787bee0af73c550716ab46e5b352'

    sender = SmsSingleSender(sms_app_id, sms_app_key)
    TEMPLATE_ID = 667205
    SMS_SIGN = "ditanshow网"

    try:
        params = [check_code]
        response = sender.send_with_param(86, mobile, TEMPLATE_ID, params, sign=SMS_SIGN, extend="", ext="")
        print("response=%s" % response)
        return response

    except Exception as e:
        print('sms error: %s' % e)
        return None


def send_code(request):
    phone_number = request.POST.get('phone_number')
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    data = {'code': 0, 'msg': "ok"}
    check_code = get_code()

    response = util_sendmsg(phone_number, check_code)
    if response["result"] == 0:
        SMSStatus(phone=phone_number, code=check_code, create_time=time_now).save()
    else:
        print("send message to %s failed" % phone_number)
        data = {'code': 1, 'msg': "发送短信失败, msg=%s" % response["errmsg"]}

    return HttpResponse(json.dumps(data), content_type="application/json")


def login_with_user_name(request):
    response = dict()
    response["msg"] = "登录成功"
    response["user"] = dict()

    username_phone = request.POST.get('username_phone', None)
    password = request.POST.get('password', None)
    print(username_phone, password)

    user_id = None
    try:
        if len(username_phone) != 11:
            raise Exception("")
        int(username_phone)
        user = UserProfile.objects.filter(phone=username_phone).values("user__id").first()
        print("%s is a modile num" % username_phone)
        if user:
            user_id = user["user__id"]
        # 手机号
    except Exception as e:
        # 用户名
        user = UserProfile.objects.filter(user__username=username_phone).values("user__id").first()
        print("%s is a username" % username_phone)
        if user:
            user_id = user["user__id"]

    if not user_id:
        response["status"] = "error"
        response["msg"] = "不存在该用户名或该手机号未注册~"
        return response

    user = User.objects.filter(id=user_id)
    if user.first().check_password(password):
        response["status"] = "success"
        response["user"] = dict()
        response["user"]["header"] = UserProfile.objects.get(user__id=user_id).header

        # 将用户信息添加到session
        request.session['user_id'] = user_id
        request.session['username'] = User.objects.get(id=user_id).username

        return response
    else:
        response["status"] = "error"
        response["msg"] = "密码错误，请重新输入"

        return response


def login_with_sms_code(request):
    response = dict()
    response["status"] = "success"
    response["msg"] = "登录成功"
    response["user"] = dict()

    mobile = request.POST.get('name_phone', None)
    code = request.POST.get('code', None)

    user = UserProfile.objects.filter(phone=mobile).values("user_id").first()
    if not user:
        response["status"] = "error"
        response["msg"] = "该手机还没有注册~"
        return response

    row = SMSStatus.objects.filter(phone=mobile, code=code).order_by("-id").values("create_time").first()
    if row:
        create_time = row["create_time"]
        response["status"] = "success"
        request.session['user_id'] = user["user_id"]
        request.session['username'] = User.objects.get(id=user["user_id"]).username
    else:
        response["status"] = "error"
        response["msg"] = "验证码错误~"

    return response


#更新密码
def update_pwd(request):
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'update_pwd.html',context={'c':c})
    elif request.method == 'POST':
        code = request.POST.get('code')
        uid = request.session.get(code)
        user = UserProfile.objects.get(pk=uid)
        pwd = request.POST.get('password')
        repwd = request.POST.get('rpassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            # request.session.flush()
            return render(request, 'update_pwd.html',context={'msg':'用户名密码更新成功！'})
        else:
            return render(request, 'update_pwd.html', context={'msg': '更新失败'})


# @login_required  #login(request, user) user-->继承Abstract
# def user_center(request):
#     user = request.user
#     if request.method == 'GET':
#         return render(request,'center.html', context={'user':user})
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         icon = request.FILES.get('icon')   #获得的只是图片的二进制信息
#         name = icon.name
#         user.username = username
#         user.email = email
#         user.mobile = mobile
#         user.icon = icon   #利用插件直接就可以保存
#         user.save()
#
#         return render(request, 'center.html', context={'user': user})
#

#图片上传到云
@login_required
def user_center(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'center.html', context={'user': user})
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get('icon')  # 获得的只是图片的二进制信息
        name = icon.name
        user.username = username
        user.email = email
        user.mobile = mobile
        # user.icon = icon  # 利用插件直接就可以保存
        #上传到七牛云
        save_path = upload_image(icon)
        user.yunicon = save_path
        user.save()
        return render(request, 'center.html', context={'user': user})


def login_qq(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        code_url = 'https://graph.qq.com/oauth2.0/authorize'
        parm = {
            'response_type': 'code',
            'client_id': '1110505456',
            'redirect_uri': 'www.ditanshouw.com/user/login/qq',
            'state':  'test'
        }
        auth_url = '%s?%s'%(code_url, urlencode(parm))
        return HttpResponseRedirect(auth_url)


#其中redirect_uri为回调url，qq服务器收到登录请求后调用你的后台实现
#www.323.com/qq  指向如下实现

#流程如下：
#1.www.323.com/login?type=qq
#2.--->跳转qq登录页面
#3.--->qq调用后台www.323.com/qq
#4.--->映射处理登录验证
#qq = QQ(^$#%%$)
#access_token = qq.get_access_token()
#openid = qq.get_openid(access_token)
#user_info = qq.get_userinfo(access_token,openid) #返回字典
#5.保持用户信息到本地数据库
#成功登录后跳转到登录前页面


#QQ登录
token_url = 'https://graph.qq.com/oauth2.0/token'
auth_url = 'https://graph.qq.com/oauth2.0/me'
class QQ(object):
    def __init__(self,appid,appkey,token_url,auth_url,user_info_url,redirect_uri,code,state):
        self.appid=appid
        self.appkey=appkey
        self.token_url=token_url
        self.auth_url=auth_url
        self.redirect_uri=redirect_uri
        self.code=code
        self.state=state
        self.user_info_url = user_info_url

    #获取access_token
    def get_access_token(self):
        parm = {
              'grant_type':'authorization_code',
                'client_id':self.appid,
                'client_secret':self.appkey,
                'redirect_uri':self.redirect_uri,
                'code':self.code
        }
        try:
            parm_token_url = '%s?%s'%(token_url, urlencode(parm))
            resp = urllib.request.urlopen(parm_token_url)
            content = resp.read()

            access_token = urllib.urlparse.parse_qs(content).get('access_token', [''])[0]
            return access_token

        except Exception as e:
            print(e.reason)

    #获取OpenID
    def get_openid(self,access_token):
        try:
            parm_auth_url = '%s?%s'%(self.auth_url, urlencode({'access_token': access_token,}))
            resp = urllib.request.urlopen(parm_auth_url)
            content = resp.read()
            content = content[content.find('(')+1:content.rfind(')')]
            data = json.loads(content)
            openid = data.get('openid')
            return openid

        except Exception as e:
            print(e)


    #获取uerinfo
    def get_userinfo(self,access_token,openid):
        parm = {
        'access_token':access_token,
        'oauth_consumer_key':self.appid,
        'openid':openid
         }
        try:
            parm_user_info_url = '%s?%s'%(self.user_info_url, urlencode(parm))
            resp = urllib.request.urlopen(parm_user_info_url)
            content = resp.read()
            user_info = json.loads(content)
            return user_info
        except Exception as e:
            print(e.reason)




