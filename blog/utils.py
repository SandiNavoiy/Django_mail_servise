from django.core.cache import cache

from blog.models import BlogPost
from config.settings import CACHE_ENABLED


def get_cached_for_blog_list():
    if CACHE_ENABLED:
        key = f'blog_list'
        object_list = cache.get(key)
        if not object_list:
            object_list = BlogPost.objects.all()
            cache.set(key, object_list, 3600)
    else:
        object_list = BlogPost.objects.all()
    return object_list
