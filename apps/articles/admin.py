from django import db, forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from apps.articles.models import Article, Tag, Category, Cover


class ArticleAdmin(admin.ModelAdmin):
    # list_display = ["title", "category", "tag_list", "date", "article_status", "click_num", "love_num", "article_surface", "upload_image", "location"]
    list_display = ["article_id", "title", "category", "date", "status", "cover_pic"]
    readonly_fields = ["article_surface", "love_num", "click_num", "location"]
    readonly_fields = []

    def cover_pic(self, obj):
        all_covers = Cover.objects.all()
        # html = '''
        #     <div>
        #         <div style="float:left; width:100px; height:100px; border: 1px solid red"></div>
        #         <div style="float:left; width:100px; height:100px; border: 1px solid red"></div>
        #     </div>
        # '''
        covers_list = ""
        for cover in all_covers:
            covers_list += """
                <tr style="background: %s">
                    <td>
                        <img style="width:90px; height:50px;" src="%s">
                    </td>
                    <td>
                        <button cover_id=%d style="margin-top:20px">选择</button>
                    </td>
                </tr>
                """ % ("white" if cover.id != obj.cover.id else "blue", cover.pic, cover.id)

        html = '''
            <style>
                tr.focus{
                    background-color:#eee;
                }
            </style>
            <script src="https://how2j.cn/study/js/jquery/2.0.0/jquery.min.js"></script>
            <div style="width:200px; height:100px; overflow:scroll">
                <table border class="cover-pic-table">
                    %s
                </table>
            </div>
            <script>
                $(".cover-pic-table tr").on("click", function () {
                    $(this).parent().find("tr.focus").toggleClass("focus");
                    $(this).toggleClass("focus");
                });
                $(".cover-pic-table button").on("click", function(){
                    $.ajax({
                        type:'POST',
                        url: "/articles/update_cover_pic",
                        data: JSON.stringify({"article_id": %d, "cover_id": parseInt($(this).attr("cover_id"))}),
                        datatype:JSON,
                        success:function (data) {alert("成功")},
                        error:function () {alert("失败")}
                    });
                });
            </script>
        ''' % (covers_list, obj.article_id)

        return mark_safe(html)

    # formfield_overrides = {models.CharField: {'widget': forms.Textarea},}
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['abstract']:
            pass
            #formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        elif db_field.name in ["cover_url"]:
            pass
            #formfield.widget = forms.ImageField()
        return formfield

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
    article_surface.allow_tags = True


class CoverAdmin(admin.ModelAdmin):
    list_display = ["id", "img"]

    def img(self, obj):
        return mark_safe('<img src="%s" style="width: 150px; height: 80px"/>' % (obj.pic))

    img.short_description = "封面"


admin.site.register(Tag)
admin.site.register(Cover, CoverAdmin)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
