from django.db import models

# Create your models here.
from libs.ckeditor.ckeditor.fields import RichTextField


class GBook(models.Model):
    id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField()
    ip = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    user_name=models.CharField(max_length=32)
    ding=models.IntegerField(default=0)
    cai=models.IntegerField(default=0)
    content=RichTextField()
    create_time = models.CharField(max_length=64)

    class Meta:
        db_table = 't_gbook'
        verbose_name = '留言板'
        verbose_name_plural = verbose_name