from django.contrib import admin

# Register your models here.
from apps.comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["title", "user_name", "address", "content", "create_time"]

admin.site.register(Comment, CommentAdmin)
