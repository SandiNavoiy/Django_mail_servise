from django.contrib import admin
from blog.models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass
    # описание отображения в админке
    list_display = ('title', 'content', 'created_at')
    # описание фильтра в админке
    list_filter = ('title', 'is_published')
    # описание доступных полей поиска в админке
    # search_fields = ('title')
    prepopulated_fields = {'slug': ('title',)}

