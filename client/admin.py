from django.apps import AppConfig

from client.models import MailingClient
from django.contrib import admin

@admin.register(MailingClient)
class MailingClientAdmin(admin.ModelAdmin):
    pass
    # описание отображения в админке
    list_display = ('contact_email', 'first_name', 'last_name', 'surname', 'comment')
    # описание фильтра в админке
    list_filter = ('contact_email', 'first_name', 'last_name', 'surname')
