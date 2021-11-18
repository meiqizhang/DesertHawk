from django.contrib import admin

from apps.statistic.models import SiteStatistic, IpCoordinate


class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ["ip_str", "url", "province", "city", "x", "y", "visit_time"]

    def ip_str(self, obj):
        return obj.coordinate.ip_str

    def province(self, obj):
        return obj.coordinate.province

    def city(self, obj):
        return obj.coordinate.city

    def x(self, obj):
        return obj.coordinate.x

    def y(self, obj):
        return obj.coordinate.y

    ip_str.short_description = "IP"
    province.short_description = "省份"
    city.short_description = "城市"
    x.short_description = '经度'
    y.short_description = '纬度'


class IpCoordinateAdmin(admin.ModelAdmin):
    list_display = ["ip_str", "province", "city", "x", "y"]


admin.site.register(IpCoordinate, IpCoordinateAdmin)
admin.site.register(SiteStatistic, SiteStatisticAdmin)
