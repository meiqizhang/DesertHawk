from django.db import models

# Create your models here.

"""
CREATE TABLE `t_document` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  `download_count` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""


class Document(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="文档名称")
    url = models.CharField(max_length=512, verbose_name="下载链接")
    create_time = models.DateTimeField(auto_created=True)
    update_time = models.DateTimeField(auto_created=True, auto_now=True)
    download_count = models.IntegerField(default='0', verbose_name="下载次数")

    class Meta:
        db_table = 't_document'
        verbose_name = '文档链接'
        verbose_name_plural = verbose_name


