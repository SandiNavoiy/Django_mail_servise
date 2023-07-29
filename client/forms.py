from django import forms
from client.models import MailingClient


class ClientForm(forms.ModelForm):
    """Форма работы с классом клиентов(получателей рассылки)"""

    class Meta:
        """подкласс описания """
        model = MailingClient  # модель
        fields = '__all__'  # поля
