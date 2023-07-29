from django.contrib.auth.models import Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создание менеджера
        user = User.objects.create(
            email = 'manager@example.ru',
            first_name = 'Manager',
            last_name = 'Manager',
            is_staff = True,
            is_superuser = False
        )
        user.set_password('kaliningrad39')  # установка пароля
        # Добавление разрешений add_blog и delete_blog
        # add_blog_permission = Permission.objects.get(codename='add_blog')
        # delete_blog_permission = Permission.objects.get(codename='delete_blog')
        # user.user_permissions.add(add_blog_permission, delete_blog_permission)
        #blog.add_blogpost

        # Сохранение менеджера в БД
        user.save()  # сохраниние в БД