from django.db import models

# Create your models here.
from libs.ckeditor.ckeditor.fields import RichTextField


class GBook(models.Model):
    STATUS_CHOICES = (
        ('p', '公开'),
        ('h', '隐藏'),
    )

    id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    ip = models.CharField(max_length=32, default="127.0.0.1")
    address = models.CharField(max_length=64, default="")
    user_name = models.CharField(max_length=32)
    ding = models.IntegerField(default=0)
    cai = models.IntegerField(default=0)
    status = models.CharField(verbose_name='评论状态', max_length=1, choices=STATUS_CHOICES, default='p')
    content = RichTextField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_gbook'
        verbose_name = '留言板'
        verbose_name_plural = verbose_name