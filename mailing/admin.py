from django.contrib import admin
from mailing.models import MailingSettings, Mail


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_status', 'mailing_time_start', 'mailing_time_start', 'mailing_periods',)
    list_filter = ('mailing_status',)
    search_fields = ('mailing_status',)


@admin.register(Mail)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('settings', 'mailing_subject', 'mailing_body')
    list_filter = ('settings',)
    search_fields = ('settings',)
