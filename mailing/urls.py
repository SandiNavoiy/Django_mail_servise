from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Home, MailingTryListView, MailingListView, MailingCreateView, MailingDeleteView

app_name = MailingConfig.name
urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('mailing_report/', MailingTryListView.as_view(), name='mailing_report'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

]
