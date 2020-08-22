from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from apps.user.models import UserProfile, VisitHistory, SMSStatus


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'header', 'phone']

    def username(self, user):
        return user.username

    def header(self, user):
        return UserProfile.objects.get(user=user).header

    def phone(self, user):
        return UserProfile.objects.get(user=user).phone

    list_per_page = 10
    username.short_description = '用户名'
    phone.short_description = '手机号'
    header.short_description = '头像'


class SMSStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "phone", "code", "create_time"]


class VisitHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "ip_str", "url", "visit_time"]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
# admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(SMSStatus, SMSStatusAdmin)
admin.site.register(VisitHistory, VisitHistoryAdmin)