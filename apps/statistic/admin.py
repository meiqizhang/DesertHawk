from django.contrib import admin

from apps.statistic.models import SiteStatistic, IpCoordinate


class SiteStatisticAdmin(admin.ModelAdmin):
    LinkingAdmin = ["province", "city", "url", "visit_time"]

    def province(self, obj):
        return obj.coordinate.province

    def city(self, obj):
        return obj.coordinate.city

    province.short_description = "省份"
    city.short_description = "城市"


class IpCoordinateAdmin(admin.ModelAdmin):
    list_display = ["province", "city", "x", "y"]


admin.site.register(IpCoordinate, IpCoordinateAdmin)
admin.site.register(SiteStatistic, SiteStatisticAdmin)
