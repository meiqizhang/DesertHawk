from django.db import models

# Create your models here.

"""
CREATE TABLE `t_site_statistic` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ip_int` INT,
  `ip_str` VARCHAR(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `province` VARCHAR(32) DEFAULT '' COMMENT '省份',
  `city` VARCHAR(64) DEFAULT '' COMMENT '城市',
  `x` VARCHAR(32) DEFAULT '0' COMMENT '经度',
  `y` VARCHAR(32) DEFAULT '0' COMMENT '维度',
  PRIMARY KEY (`id`),
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
) ENGINE=INNODB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8

"""
class SiteStatistic(models.Model):
    ip_int = models.IntegerField(verbose_name="IP的10分进制")
    ip_str = models.CharField(max_length=32)
    province = models.CharField(max_length=32, verbose_name="省份")
    city = models.CharField(max_length=32, verbose_name="市/区")
    x = models.CharField(max_length=16, verbose_name='经度')
    y = models.CharField(max_length=16, verbose_name='维度')
    visit_time = models.CharField(max_length=32, default='', verbose_name="访问时间")

    class Meta:
        db_table = 't_site_statistic'
        verbose_name = "访客统计"
        verbose_name_plural = verbose_name


class CityCoordinate(models.Model):
    province = models.CharField(max_length=32, verbose_name="省份")
    city = models.CharField(max_length=32, verbose_name="市/区")
    x = models.CharField(max_length=16, verbose_name='经度')
    y = models.CharField(max_length=16, verbose_name='维度')

    class Meta:
        db_table = 't_city_coordinate'
        verbose_name = "城市经纬度坐标"
        verbose_name_plural = verbose_name
