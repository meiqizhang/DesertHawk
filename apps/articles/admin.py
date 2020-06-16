from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from apps.articles.models import Article, Tag, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "first_category", "second_category", "tag_list", "date", "click_num", "love_num", "admin_image", "location"]
    #raw_id_fields = ["first_category"]
    readonly_fields = ['admin_image']

    def location(self, obj):
        pass

    def tag_list(self, obj):
        try:
            tags = eval(obj.tags)
        except Exception as e:
            tags = []

        print(tags)
        show_list = ''
        if isinstance(tags, list):
            for tag in tags:
                show_list += '<span style="margin: 10px; padding: 4px; border: 1px solid grey">' + tag + '</span>'
        else:
            show_list = '<span style="color: red">无效标题</span>'
        return mark_safe(show_list)

    def admin_image(self, obj):
        return mark_safe('<img src="%s" style="width: 150px; height: 80px" />' % ("/articles/d_icon/?title=" + obj.title))

    list_per_page = 10
    tag_list.short_description = "标签"
    admin_image.short_description = "封面图片"
    admin_image.allow_tags = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["title", "tag"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
