import os
import time

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files import File
from django.core.files.storage import Storage
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.utils.safestring import mark_safe

#from apps.articles.views import upload_icon
from qcloud_cos import CosConfig, CosS3Client

from DesertHawk.settings import BASE_DIR, cos_client
from db_tool import db_connect
from libs.mdeditor.fields import MDTextField

"""
CREATE TABLE `t_tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq` (`tag`,`title`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8
"""

class Tag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='标签')
    title = models.CharField(max_length=64, verbose_name="文章title")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_tag'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name


class ContentImage(models.Model):
    md5 = models.CharField(max_length=64, verbose_name="图片MD5")
    image = models.ImageField(verbose_name='图片二进制')

    class Meta:
        db_table = "t_content_image"

"""
CREATE TABLE `t_article` (
  `id` 		INT NOT NULL AUTO_INCREMENT,
  `title` 	VARCHAR(128) NOT NULL,
  `category` 	VARCHAR(32) DEFAULT '文章分类',
  `tags` 	VARCHAR(64) DEFAULT '[]' COMMENT '文章标签',
  `description` VARCHAR(1024) DEFAULT '',
  `content` 	MEDIUMTEXT,
  `click_num` 	INT DEFAULT '0',
  `love_num` 	INT DEFAULT '0',
  `date` 	VARCHAR(32) DEFAULT '' COMMENT '文章发布时间',
  `image` 	MEDIUMBLOB COMMENT '二进制图片',
  `image_url` VARCHAR(256) DEFAULT '' comment '图标url'
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=INNODB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

"""class SaveIcon(Storage):

    def save(self, name, content, max_length=None):
        #content = File(content, name)
        save_path = os.path.join(BASE_DIR, "media/articles/thumb/%s" % name)

        with open(save_path, 'wb') as f:
            for chunk in content.chunks():
                f.write(chunk)

        return save_path

    def url(self, name):
        return "https://pic1.zhimg.com/80/v2-635f64d3b355482ec8853610479d3a14_720w.png"
"""

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=64, verbose_name="一级分类")
    create_time = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 't_category'
        verbose_name = '文章一级分类表'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    first_category = models.CharField(max_length=32, default="程序设计", verbose_name="一级分类")
    second_category = models.CharField(max_length=32, default="", verbose_name="二级分类")
    tags = models.CharField(max_length=64, verbose_name='文章标签')
    description = models.CharField(max_length=256, verbose_name='简介')
    content = MDTextField(verbose_name='文章正文')
    date = models.DateTimeField(verbose_name='发表日期', auto_now=True)
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    love_num = models.IntegerField(default=0, verbose_name='点赞量')
    #image = models.ImageField(verbose_name='文章图标')
    location = models.CharField(max_length=32, verbose_name="地理位置")
    status = models.IntegerField(default=0, verbose_name="文章状态")
    #first_category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, verbose_name=u'文章类别')

    class Meta:
        db_table = 't_article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        response = cos_client.put_object(
            Bucket='article-1251916339',
            Body=self.content,
            Key=self.title + '-%s.md' % time_now,
            EnableMD5=False
        )
        super().save(*args, **kwargs)

"""
CREATE TABLE `t_site_statistic` (
  `ip_int` BIGINT NOT NULL AUTO_INCREMENT,
  `ip_str` VARCHAR(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `province` VARCHAR(32) DEFAULT '' COMMENT '省份',
  `city` VARCHAR(64) DEFAULT '' COMMENT '城市',
  `x` FLOAT DEFAULT '0' COMMENT '经度',
  `y` FLOAT DEFAULT '0' COMMENT '维度',
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `ip_int` (`ip_int`,`create_time`)
) ENGINE=INNODB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8
"""

"""
CREATE TABLE `t_article_index` (
  `score` float DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `content` mediumtext,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` int DEFAULT NULL,
  FULLTEXT KEY `fulltext_title_content` (`title`,`content`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `title_indx` (`title`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `title_index` (`title`) /*!50100 WITH PARSER `ngram` */ ,
  FULLTEXT KEY `content_index` (`content`) /*!50100 WITH PARSER `ngram` */ 
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC

"""

class ArticleIndex(models.Model):
    title = models.CharField(max_length=128, verbose_name='文章标题')
    content = models.TextField(max_length=1024*1024*4, verbose_name='文章内容')

    class Meta:
        db_table = 't_article_index'
        verbose_name = '文章索引'
        verbose_name_plural = verbose_name
