from django.contrib import admin

from posts.models import Comment, Follow, Group, Post

admin.site.empty_value_display = '-пусто-'


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', 'author')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'post', 'author', 'created')
    search_fields = ('text', 'post', 'author')
    list_filter = ('author', 'created')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
