from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import Home, MailingTryListView, MailingListView, MailingCreateView, MailingDeleteView, \
    MailingUpdateView

app_name = MailingConfig.name
urlpatterns = [
    path('', cache_page(1)(Home.as_view()), name='index'),
    path('mailing_report/', MailingTryListView.as_view(), name='mailing_report'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),

]
