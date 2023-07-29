from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Home, MailingTryListView

app_name = MailingConfig.name
urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('mailing_report/', MailingTryListView.as_view(), name='mailing_report'),

]
