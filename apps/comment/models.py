from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.

"""
CREATE TABLE `t_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `parent_id` int DEFAULT '-1',
  `user_name` varchar(32) NOT NULL,
  `content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""


class Comment(models.Model):
    ip = models.CharField(max_length=32, verbose_name="ip地址")
    address = models.CharField(max_length=64, verbose_name="ip地址所在地区")
    title = models.CharField(max_length=128, verbose_name="文章标题")
    parent_id = models.IntegerField(verbose_name="父级id", default=-1)
    user_name = models.CharField(max_length=32, verbose_name="用户")
    ding = models.IntegerField(default=0)
    cai = models.IntegerField(default=0)
    content = RichTextField(verbose_name="评论内容")
    create_time = models.CharField(max_length=32, verbose_name="创建时间")

    class Meta:
        db_table = 't_comment'
        verbose_name = '文章评论表'
        verbose_name_plural = verbose_name