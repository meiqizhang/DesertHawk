from django.contrib import admin

# Register your models here.
from apps.document.models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "create_time", "download_count"]

admin.site.register(Document, DocumentAdmin)

