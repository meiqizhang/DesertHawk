from django.db import models

# Create your models here.

class VisitUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    phone = models.CharField(max_length=16, verbose_name="手机号")
    header_url = models.CharField(max_length=256, verbose_name="头像链接")
    class Meta:
        db_table = 't_visit_user'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name