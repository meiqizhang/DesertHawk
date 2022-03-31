from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from apps.photos.models import Photo, PhotoCategory


class PhotoCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "permission", "cover_pic"]

    def cover_pic(self, obj):
        return mark_safe('<img src="%s" style="width: 150px; height: 80px"/>' % (obj.cover.pic))

    cover_pic.short_description = "分类封面"


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "thumbnail"]

    def thumbnail(self, obj):
        url = obj.photo
        return mark_safe('<img src="%s" style="width: 150px; height: 80px"/>' % url)

    thumbnail.short_description = "相片"


admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoCategory, PhotoCategoryAdmin)

