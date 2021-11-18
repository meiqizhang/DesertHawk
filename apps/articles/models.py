import os
import time
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from libs.mdeditor.fields import MDTextField


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='标签', default="", unique=True)

    class Meta:
        db_table = 't_tag'
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
        image_buf = content.file.getvalue()

        secret_id = os.environ.get("COS_SECRET_ID", None)
        secret_key = os.environ.get("COS_SECRET_KEY", None)
        secret_id = None
        if secret_id is None or secret_key is None:
            cover_path = settings.MEDIA_ROOT + "/cover-pic/"
            if not os.path.exists(cover_path):
                os.makedirs(cover_path)
            with open(cover_path + filename, "wb") as fp:
                fp.write(image_buf)
            return settings.MEDIA_URL + "/cover-pic/" + filename
        else:
            from qcloud_cos import CosConfig, CosS3Client
            config = CosConfig(Region='ap-beijing', SecretId=secret_id, SecretKey=secret_key)
            cos_client = CosS3Client(config)
            response = cos_client.put_object(
                Bucket='blog-1251916339',
                Body=content,
                Key='/cover-pic/' + filename,
                EnableMD5=False
            )
            return "https://blog-1251916339.cos.ap-beijing.myqcloud.com/cover-pic/" + filename


class Cover(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(verbose_name="分类", max_length=32, default=None)
    pic = models.ImageField(verbose_name="封面图片", default=None, storage=MyStorage())

    class Meta:
        db_table = 't_cover'
        verbose_name = '文章封面'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pic)


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
    content = MDTextField()
    #content = MDTextField(verbose_name='文章正文')
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
        # time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
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

