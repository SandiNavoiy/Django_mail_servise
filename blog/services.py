from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


# def cached_for_blog():
#     if CACHE_ENABLED:
#         key = f'blog_post_list'
#         object_list = cache.get(key)
#
#         if object_list is None:
#             # Если данные не найдены в кеше, выполняем запрос к базе данных
#             object_list = BlogPost.objects.all()
#             # Кешируем результат на 1 час
#             cache.set(key, object_list)
#     else:
#         object_list = BlogPost.objects.all()
#
#     return object_list