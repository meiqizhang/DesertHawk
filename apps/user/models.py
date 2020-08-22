from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, verbose_name="手机号")
    header = models.CharField(max_length=256, verbose_name="头像链接")

    def __str__(self):
        return self.user.id

    class Meta:
        db_table = 't_user_profile'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


class SMSStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(max_length=16, verbose_name="手机号")
    code = models.CharField(max_length=8, verbose_name="验证码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        db_table = 't_sms_status'
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name


class VisitHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    ip_str = models.CharField(max_length=32)
    url = models.CharField(max_length=512, verbose_name="访问的url")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    class Meta:
        db_table = "t_visit_history"
        verbose_name = "用户访问历史"
        verbose_name_plural = verbose_name