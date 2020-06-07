# Generated by Django 2.2.12 on 2020-06-06 16:08

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('category', models.CharField(max_length=32, verbose_name='文章分类')),
                ('tags', models.CharField(max_length=64, verbose_name='文章标签')),
                ('description', models.CharField(max_length=256, verbose_name='简介')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容')),
                ('date', models.CharField(max_length=32, verbose_name='发表日期')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
                ('love_num', models.IntegerField(default=0, verbose_name='点赞量')),
                ('image', models.ImageField(upload_to='', verbose_name='图片二进制')),
            ],
            options={
                'verbose_name': '文章表',
                'verbose_name_plural': '文章表',
                'db_table': 't_article',
            },
        ),
        migrations.CreateModel(
            name='ArticleIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('content', models.TextField(max_length=4194304, verbose_name='文章内容')),
            ],
            options={
                'verbose_name': '文章索引',
                'verbose_name_plural': '文章索引',
                'db_table': 't_article_index',
            },
        ),
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=64, verbose_name='图片MD5')),
                ('image', models.ImageField(upload_to='', verbose_name='图片二进制')),
            ],
            options={
                'db_table': 't_content_image',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, verbose_name='标签')),
                ('title', models.CharField(max_length=64, verbose_name='文章title')),
            ],
            options={
                'verbose_name': '标签表',
                'verbose_name_plural': '标签表',
                'db_table': 't_tag',
            },
        ),
    ]