# -*- coding:utf-8 -*-
import logging
import os
import datetime
import time
import uuid

from django.views import generic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .configs import MDConfig

# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def post_old(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # image none check
        if not upload_image:
            return JsonResponse({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            })

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return JsonResponse({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            })

        # image floder check
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS['image_folder'])
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return JsonResponse({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                })

        # save image
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),
                                       file_extension)
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:
            for chunk in upload_image.chunks():
                file.write(chunk)

        return JsonResponse({'success': 1,
                             'message': "上传成功！",
                             'url': os.path.join(settings.MEDIA_URL,
                                                 MDEDITOR_CONFIGS['image_folder'],
                                                 file_full_name)})

    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # image none check
        if not upload_image:
            return JsonResponse({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            })

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return JsonResponse({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            })

        # image floder check
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS['image_folder'])
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return JsonResponse({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                })

        # save image
        save_path = "{0}/".format(time.strftime("%Y/%m/%d"), str(uuid.uuid4()).replace('-', ''))
        new_name = "{0}.{1}".format(str(uuid.uuid4()).replace('-', ''), file_extension)
        image_buf = upload_image.read()
        secret_id = os.environ.get("COS_SECRET_ID", None)
        secret_key = os.environ.get("COS_SECRET_KEY", None)
        if secret_id is None or secret_key is None:
            image_path = settings.MEDIA_ROOT + "/blog-pic/" + save_path
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            with open(image_path + new_name, "wb") as fp:
                fp.write(image_buf)
            url = settings.MEDIA_URL + "/blog-pic/" + save_path + new_name
        else:
            from qcloud_cos import CosConfig, CosS3Client
            config = CosConfig(Region='ap-beijing', SecretId=secret_id, SecretKey=secret_key)
            cos_client = CosS3Client(config)
            response = cos_client.put_object(
                Bucket='blog-1251916339',
                Body=image_buf,
                Key='/blog-pic/' + save_path + new_name,
                EnableMD5=False
            )
            url = "https://blog-1251916339.cos.ap-beijing.myqcloud.com/blog-pic/" + save_path + new_name

        return JsonResponse({'success': 1, 'message': "上传成功！", 'url': url})
