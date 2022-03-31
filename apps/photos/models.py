import io
import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models

from DesertHawk.settings import MEDIA_URL,  MEDIA_ROOT
from apps.articles.models import Cover

from PIL import Image
from io import BytesIO


class PhotoCategory(models.Model):
    PERMISSION_CHOICES = (
        (0, '隐藏'),
        (1, '公开'),
    )

    id = models.AutoField(primary_key=True)
    category = models.CharField(verbose_name="分类", max_length=32, default=None)
    description = models.CharField(verbose_name="描述", max_length=512, default="")
    permission = models.IntegerField(verbose_name='权限', choices=PERMISSION_CHOICES, default=1)
    cover = models.ForeignKey(Cover, verbose_name='相册封面', default=None, on_delete=models.PROTECT)

    class Meta:
        db_table = 't_photo_category'
        verbose_name = '相册名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class PhotoStorage(FileSystemStorage):
    def _save(self, name, content):
        filename = name.replace('\\', '/')
        if isinstance(content, TemporaryUploadedFile):
            image_buf = content.read(content.size)
        else:
            image_buf = content.file.getvalue()
        preview_image = Image.open(BytesIO(image_buf))

        # 高度和宽度至少有一个小于1024
        while True:
            height = preview_image.height
            width = preview_image.width
            preview_image.thumbnail((height * 0.8, width * 0.8), Image.ANTIALIAS)
            if preview_image.height <= 1024 or preview_image.width <= 1024:
                break
        img_byte = io.BytesIO()
        preview_image.save(img_byte, format='PNG')
        preview_content = img_byte.getvalue()

        thumb_image = Image.open(BytesIO(image_buf))
        thumb_image.thumbnail((200, 150), Image.ANTIALIAS)

        img_byte = io.BytesIO()
        thumb_image.save(img_byte, format='PNG')
        thumb_content = img_byte.getvalue()

        secret_id = os.environ.get("COS_SECRET_ID", None)
        secret_key = os.environ.get("COS_SECRET_KEY", None)
        if secret_id is None or secret_key is None:
            original_path = MEDIA_ROOT + "/photos/original/"
            if not os.path.exists(original_path):
                os.makedirs(original_path)
            with open(original_path + filename, "wb") as fp:
                fp.write(image_buf)

            preview_path = MEDIA_ROOT + "/photos/preview/"
            if not os.path.exists(preview_path):
                os.makedirs(preview_path)
            with open(preview_path + filename, "wb") as fp:
                fp.write(preview_content)

            thumbnail_path = MEDIA_ROOT + "/photos/thumbnail/"
            if not os.path.exists(thumbnail_path):
                os.makedirs(thumbnail_path)
            with open(thumbnail_path + filename, "wb") as fp:
                fp.write(thumb_content)
            return MEDIA_URL + "/photos/thumbnail/" + filename
        else:
            from qcloud_cos import CosConfig, CosS3Client
            config = CosConfig(Region='ap-beijing', SecretId=secret_id, SecretKey=secret_key)
            cos_client = CosS3Client(config)

            response = cos_client.put_object(
                Bucket='blog-1251916339',
                Body=image_buf,
                Key='/photos/original/' + filename,
                EnableMD5=False
            )

            response = cos_client.put_object(
                Bucket='blog-1251916339',
                Body=preview_content,
                Key='/photos/preview/' + filename,
                EnableMD5=False
            )

            response = cos_client.put_object(
                Bucket='blog-1251916339',
                Body=thumb_content,
                Key='/photos/thumbnail/' + filename,
                EnableMD5=False
            )
            return "https://blog-1251916339.cos.ap-beijing.myqcloud.com/photos/thumbnail/" + filename


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('PhotoCategory', verbose_name="分类", max_length=32, default=None, on_delete=models.PROTECT)
    photo = models.ImageField(verbose_name="照片", default=None, max_length=1024, storage=PhotoStorage())

    class Meta:
        db_table = 't_photos'
        verbose_name = '相册照片'
        verbose_name_plural = verbose_name

