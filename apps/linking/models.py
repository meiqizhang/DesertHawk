from django.db import models

# Create your models here.

# class Comment(models.Model):
#     ip = models.CharField(max_length=32, verbose_name="ip地址")
#     address = models.CharField(max_length=64, verbose_name="ip地址所在地区")
#     title = models.CharField(max_length=128, verbose_name="文章标题")
#     parent_id = models.IntegerField(verbose_name="父级id", default=-1)
#     user_name = models.CharField(max_length=32, verbose_name="用户")
#     ding = models.IntegerField(default=0)
#     cai = models.IntegerField(default=0)
#     content = RichTextField(verbose_name="评论内容")
#     create_time = models.CharField(max_length=32, verbose_name="创建时间")
#
#     class Meta:
#         db_table = 't_comment'
#         verbose_name = '文章评论表'
#         verbose_name_plural = verbose_name


class Linking(models.Model):
    STATUS_CHOICES = (
        (0, '无效'),
        (1, '生效'),
    )

    id = models.AutoField(primary_key=True)
    href = models.CharField(max_length=128, verbose_name="地址")
    title = models.CharField(max_length=128, verbose_name="标题", default=None)
    name = models.CharField(max_length=64, verbose_name="网站名")
    status = models.IntegerField(verbose_name='状态', choices=STATUS_CHOICES, default='1')

    class Meta:
        db_table = "t_linking"
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name
