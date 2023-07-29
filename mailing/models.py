from django.db import models
from django.db.models import TextChoices
from blog.models import NULLABLE
from client.models import MailingClient
from config.settings import AUTH_USER_MODEL


class Status(TextChoices):
    '''Возможный статус рассылки'''
    ACTIVE = 'AC', 'Active'
    FINISHED = 'FI', 'Finished'
    CREATED = 'CR', 'Created'


class Periods(TextChoices):
    '''Возможные  периодичности рассылки'''
    DAILY = 'DL', 'Daily'
    WEEKLY = 'WL', 'Weekly'
    MONTHLY = 'ML', 'Monthly'


class MailingSettings(models.Model):
    '''Настройка рассылки'''
    mailing_status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREATED,
                                      verbose_name='статус рассылки')
    mailing_time_start = models.DateTimeField(verbose_name='время начала рассылки', **NULLABLE)
    mailing_time_end = models.DateTimeField(verbose_name='время конца рассылки', **NULLABLE)
    mailing_periods = models.CharField(max_length=2, choices=Periods.choices, verbose_name='периодичность')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.mailing_status}({self.mailing_time_start}), {self.mailing_periods}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
        ordering = ["mailing_status"]


class Mail(models.Model):
    '''Письмо рассылки'''
    client_to_message = models.ManyToManyField(MailingClient, verbose_name='Клиенты',
                                               related_name='client_to_message')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    mailing_subject = models.CharField(max_length=255, verbose_name='тема письма')
    mailing_body = models.CharField(max_length=500, verbose_name='тело письма')
    all_clients = models.BooleanField(verbose_name='все клиенты', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.mailing_subject}: {self.mailing_body}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingTry(models.Model):
    '''Логи рассылки'''
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    mailing_try = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    mailing_try_status = models.CharField(max_length=255, verbose_name='статус рассылки', **NULLABLE)
    mailing_response = models.CharField(max_length=255, verbose_name='ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_try.strftime("%d.%m.%Y %H:%M")} ({self.mailing_try_status}): {self.mailing_response}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
