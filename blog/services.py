from uuid import uuid4
from pytils.translit import slugify


from django.core.cache import cache
from blog.models import BlogPost
from config.settings import CACHE_ENABLED


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def cached_for_blog():
    pass
    # if CACHE_ENABLED:
    #     key = f'blog_post_list'
    #     object_list = cache.get(key)
    #
    #     if not object:
    #         # Если данные не найдены в кеше, выполняем запрос к базе данных
    #         object_list = BlogPost.objects.all()
    #         # Кешируем результат на 1 час
    #         cache.set(key, object_list, 3600)
    # else:
    #     object_list = BlogPost.objects.all()
    #
    # return object_list