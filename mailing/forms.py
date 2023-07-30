from django.forms import ModelForm, ModelMultipleChoiceField, DateTimeInput
from client.models import MailingClient
from mailing.models import Mail, MailingSettings
from django import forms


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # для случая когда данные уже есть, чтобы не показывать виджет
        instance = kwargs.get('instance')

        if instance:
            # Получаем значения полей, если они есть
            mailing_time_start = instance.mailing_time_start
            mailing_time_end = instance.mailing_time_end

            # Проверяем наличие значений и присваиваем их полям виджетов
            if mailing_time_start:
                self.fields['mailing_time_start'].widget = forms.TextInput(
                    attrs={'value': mailing_time_start.strftime('%Y-%m-%dT%H:%M')})
            if mailing_time_end:
                self.fields['mailing_time_end'].widget = forms.TextInput(
                    attrs={'value': mailing_time_end.strftime('%Y-%m-%dT%H:%M')})


