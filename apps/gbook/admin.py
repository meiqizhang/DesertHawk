from django.contrib import admin

# Register your models here.
from apps.gbook.models import GBook


class GBookAdmin(admin.ModelAdmin):
    list_display = ["status", "address", "content", "create_time"]


admin.site.register(GBook, GBookAdmin)
