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
    comment = models.TextField(verbose_name='комментарий',**NULLABLE)
    first_name = models.CharField(max_length=25, verbose_name='имя')
    last_name = models.CharField(max_length=25, verbose_name='фамилия', **NULLABLE)

    # переопределение поля user  как основного для идентификации на емаил
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
