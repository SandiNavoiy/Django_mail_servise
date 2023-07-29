from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Home

app_name = MailingConfig.name
urlpatterns = [
    path('', Home.as_view(), name='index'),

]
