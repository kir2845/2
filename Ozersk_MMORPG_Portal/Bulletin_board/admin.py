from django.contrib import admin
from .models import Category, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time_in')
    list_filter = ('name', 'author', 'time_in')


admin.site.register(Category)
admin.site.register(Post)
#admin.site.register(Post, PostAdmin)
admin.site.register(Comment)




