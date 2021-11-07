from django.db import models

# Create your models here.


class IpCoordinate(models.Model):
    id = models.AutoField(primary_key=True)
    ip_str = models.CharField(verbose_name="ip地址", max_length=32, default=None, unique=True)
    province = models.CharField(max_length=32, verbose_name="省份")
    city = models.CharField(max_length=32, verbose_name="市/区")
    x = models.CharField(max_length=16, verbose_name='经度')
    y = models.CharField(max_length=16, verbose_name='维度')

    class Meta:
        db_table = 't_ip_coordinate'
        verbose_name = "城市经纬度坐标"
        verbose_name_plural = verbose_name


class SiteStatistic(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(verbose_name="访问地址", max_length=512, default=None)
    coordinate = models.ForeignKey(IpCoordinate, default=None, on_delete=models.DO_NOTHING)
    visit_time = models.DateTimeField(max_length=32, verbose_name="访问时间", auto_now_add=True)

    class Meta:
        db_table = 't_site_statistic'
        verbose_name = "访客统计"
        verbose_name_plural = verbose_name


