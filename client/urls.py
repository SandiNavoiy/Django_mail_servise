from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientsDetailView
from django.urls import path

app_name = ClientConfig.name
urlpatterns = [
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientsDetailView.as_view(), name='client_detail'),
]
