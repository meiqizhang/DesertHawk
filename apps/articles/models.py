import os
import time
from django import db
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage, FileSystemStorage
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# from apps.articles.views import upload_icon
from qcloud_cos import CosConfig, CosS3Client

from DesertHawk.settings import BASE_DIR, cos_client
from db_tool import db_connect
from libs.mdeditor.fields import MDTextField


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=32, verbose_name='标签', default="", unique=True)

    class Meta:
        db_table = 't_tag'
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='分类', max_length=30, unique=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="父级分类",
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    class Meta:
        db_table = 't_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MyStorage(FileSystemStorage):
    def _save(self, name, content):
        filename = name.replace('\\', '/')
        content = content.file.getvalue()
        print(filename, content)
        # Cover(pic_buf=content).save()
        # with db.connection.cursor() as cur:
        #     ret = cur.execute("insert into t_cover(`pic_buf`) value (%s)" % content)
        #     print(ret)
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        response = cos_client.put_object(
            Bucket='article-1251916339',
            Body=content,
            Key=filename,
            EnableMD5=False
        )
        return "https://article-1251916339.cos.ap-beijing.myqcloud.com/" + filename


class Cover(models.Model):
    id = models.AutoField(primary_key=True)
    pic = models.ImageField(verbose_name="封面图片", default=None, storage=MyStorage())

    class Meta:
        db_table = 't_cover'
        verbose_name = '文章封面'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pic)
        # return mark_safe('<img src="%s" style="width: 100px; height:100px" />' % self.pic_buf)


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )

    article_id = models.IntegerField(default=0, verbose_name="文章id", unique=True)
    title = models.CharField(max_length=128, verbose_name='标题')
    category = models.ForeignKey(Category, default=None, verbose_name="文章分类", on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', verbose_name='文章标签', blank=True)
    abstract = models.CharField(verbose_name='摘要', max_length=512, default=None)
    content = MDTextField(verbose_name='文章正文')
    date = models.DateTimeField(verbose_name='发表日期')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    love_num = models.IntegerField(default=0, verbose_name='点赞量')
    status = models.CharField(verbose_name='文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    cover = models.ForeignKey(Cover, verbose_name="封面", default=None, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 't_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # response = cos_client.put_object(
        #     Bucket='article-1251916339',
        #     Body=self.content,
        #     Key=self.title + '-%s.md' % time_now,
        #     EnableMD5=False
        # )

        if Article.objects.filter(title=self.title).values("article_id").first():
            self.article_id = Article.objects.filter(title=self.title).values("article_id").first()["article_id"]
        else:
            if not Article.objects.first():
                self.article_id = 1
            else:
                self.article_id = Article.objects.values("article_id").order_by("-article_id").first()["article_id"] + 1

        super().save(*args, **kwargs)


