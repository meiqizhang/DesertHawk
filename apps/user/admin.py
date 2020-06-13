from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from apps.user.models import UserProfile


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


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
admin.site.register(UserProfile, ProfileAdmin)