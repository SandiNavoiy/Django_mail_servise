from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import Home

app_name = MailingConfig.name
urlpatterns = [
    path('', Home.as_view(), name='index'),
    # path('create_cat', CategoryCreateView.as_view(), name='create_cat'),
    # path('categorii', CategoriiListView.as_view(), name='categorii'),
    # path('mail_report/', LogListView.as_view(), name='mail_report'),
    # path('client_create/', ClientCreateView.as_view(), name='client_create'),
    # path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    # path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # path('client_list/', ClientListView.as_view(), name='client_list'),
    # path('client_detail/<int:pk>/', ClientsDetailView.as_view(), name='client_detail'),
    #


]
