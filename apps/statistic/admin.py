from django.contrib import admin

from apps.statistic.models import SiteStatistic, CityCoordinate


class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ["ip_str", "province", "city", "x", "y", "visit_time"]


class CityCoordinateAdmin(admin.ModelAdmin):
    list_display = ["province", "city", "x", "y"]


admin.site.register(CityCoordinate, CityCoordinateAdmin)
admin.site.register(SiteStatistic, SiteStatisticAdmin)
