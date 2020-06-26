from django.contrib import admin

from apps.statistic.models import SiteStatistic


class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ["ip_str", "province", "city", "x", "y", "visit_time"]


admin.site.register(SiteStatistic, SiteStatisticAdmin)
