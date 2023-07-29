from django.forms import ModelForm, ModelMultipleChoiceField, DateTimeInput

from client.models import MailingClient
from mailing.models import Mail, MailingSettings


class MailForm(ModelForm):
    '''Форма для письма с переменной которая выводит в список и дает выбрать нескольких клиентов'''
    clients = MailingClient.objects.all()
    client_to_message = ModelMultipleChoiceField(queryset=clients, required=False)

    class Meta:
        model = Mail
        fields = ('mailing_subject', 'mailing_body', 'client_to_message', 'all_clients',)


class SettingsForm(ModelForm):
    '''Форма для настроек рассылки'''

    class Meta:
        model = MailingSettings
        fields = ('mailing_time_start', 'mailing_time_end', 'mailing_periods',)
        widgets = {
            'mailing_time_start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'mailing_time_end': DateTimeInput(attrs={'type': 'datetime-local'})}