from django.contrib import admin

# Register your models here.
from apps.linking.models import Linking


class LinkingAdmin(admin.ModelAdmin):
    list_display = ["name", "href", "title",  "status"]


admin.site.register(Linking, LinkingAdmin)
