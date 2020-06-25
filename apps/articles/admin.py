from django import db
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from apps.articles.models import Article, Tag, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "first_category", "second_category", "tag_list", "date", "article_status", "click_num", "love_num", "article_surface", "upload_image", "location"]
    #raw_id_fields = ["first_category"]
    readonly_fields = ["article_surface", "love_num", "click_num", "location"]

    def location(self, obj):
        pass

    def article_status(self, obj):
        if obj.status == 0:
            return "草稿箱"
        else:
            return "已发表"

    def tag_list(self, obj):
        try:
            tags = eval(obj.tags)
        except Exception as e:
            tags = []

        show_list = ''
        if isinstance(tags, list):
            for tag in tags:
                show_list += '<span style="margin: 10px; padding: 4px; border: 1px solid grey">' + tag + '</span>'
        else:
            show_list = '<span style="color: red">无效标题</span>'
        return mark_safe(show_list)

    def upload_image(self, obj):
        title = obj.title
        html = '<script src="https://how2j.cn/study/js/jquery/2.0.0/jquery.min.js"></script>'\
               '<script>'\
                    'function upload_%d(title) {' \
                        'var formData = new FormData();'\
                        'var file_obj = document.getElementById("id-%d").files[0];' \
                        'formData.append("file", file_obj);' \
                        'formData.append("id", "%d");' \
                        '$.ajax({    '\
                             'url: "/articles/u_icon/", '\
                             'data: formData, ' \
                             'type: "POST",  '\
                             'processData: false,'\
                             'contentType: false,'\
                             'dataType: "JSON",'\
                             'success: function(data) {alert(data.msg);},'\
                             'error: function(data) {alert(data.msg);}'\
                             '});'\
                    '};'\
                '</script>'\
                '<input type="file" id="id-%d" /><br>'\
                '<input type="button" value="上传" onclick=upload_%d("%d") />' % (obj.id, obj.id, obj.id, obj.id, obj.id, obj.id)

        return mark_safe(html)

    def article_surface(self, obj):
        url = "/articles/d_icon/?title=" + obj.title

        url = url.replace("+", "%2B")
        url = url.replace('&', "%26")
        url = url.replace('#', "%23")

        return mark_safe('<img src="%s" style="width: 150px; height: 80px" onclick="alert()"/>' % url)
        #record = Article.objects.raw("select id, image from t_article where title=%s", [obj.title])[0]
        return mark_safe('<img src="%s" style="width: 150px; height: 80px" onclick="alert()"/>' % (record.image))

    list_per_page = 10
    tag_list.short_description = "标签"
    article_surface.short_description = "封面图片"
    upload_image.short_description = "上传封面"
    article_status.short_description = "文章状态"
    article_surface.allow_tags = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["title", "tag"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
