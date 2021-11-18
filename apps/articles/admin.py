from django import db, forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from apps.articles.models import Article, Tag, Category, Cover


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["article_id", "title", "first_category", "second_category", "tag_list", "date",
                    "status", "love_num", "click_num", "cover_pic"]

    def first_category(self, obj):
        if obj.category.parent is None:
            return obj.category
        else:
            return obj.category.parent

    def second_category(self, obj):
        if obj.category.parent is None:
            return ""
        else:
            return obj.category

    def tag_list(self, obj):
        show_list = ''
        for tag in obj.tags.all():
            show_list += '<span style="margin: 5px; padding: 4px; border: 1px solid grey">%s</span>' % tag
        return mark_safe(show_list)

    def cover_pic(self, obj):
        return mark_safe('<img src="%s" style="width: 150px; height: 80px" onclick="alert()"/>' % obj.cover.pic)

    list_per_page = 10
    first_category.short_description = "一级分类"
    second_category.short_description = "二级分类"
    tag_list.short_description = "标签"
    cover_pic.short_description = "封面图片"
    cover_pic.allow_tags = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "parent"]


class CoverAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "img"]

    def img(self, obj):
        return mark_safe('<img src="%s" style="width: 150px; height: 80px"/>' % (obj.pic))

    img.short_description = "封面"


admin.site.register(Tag)
admin.site.register(Cover, CoverAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
