from django.contrib.auth.models import AbstractUser
from django.db import models

# создание флага необязательного поля
NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=20, verbose_name='страна', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    first_name = models.CharField(max_length=25, verbose_name='имя')
    last_name = models.CharField(max_length=25, verbose_name='фамилия', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')

    # переопределение поля user  как основного для идентификации на емаил
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    class StatusType(models.Model):
        '''Подкласс для определения роли пользователя'''
        MANAGER = "MANAGER"
        BASE_USER = "BASE_USER"
        CONTENT_MANAGER = "CONTENT_MANAGER"
        STATUS = [
            (MANAGER, "Manager"),
            (BASE_USER, "Base_user"),
            (CONTENT_MANAGER, "Content_manager"),
        ]

    status_type = models.CharField(
        max_length=50,
        choices=StatusType.STATUS,
        default=StatusType.BASE_USER,
        verbose_name="роль")
