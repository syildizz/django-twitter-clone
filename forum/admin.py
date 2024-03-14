from django.contrib import admin
from .models import Message

#admin.site.register(Message, None)

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_active', 'reply_to', 'content', 'likes_count', 'dislikes_count', 'pub_date', 'edit_date')
    list_filter = ('reply_to', 'is_active', 'pub_date', 'edit_date')
    fields = ['author', 'is_active', 'reply_to', 'content', ('likes', 'dislikes'), 'edit_date']
