from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.defaultfilters import slugify
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from client.forms import ClientForm
from client.models import MailingClient


# Работа с получателями рассылок
# ---------------------------------------------------------------------------------
class ClientCreateView(LoginRequiredMixin, CreateView):
    '''Создание получателя рассылки'''
    template_name = "client/create_clients.html"
    model = MailingClient
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')


class ClientListView(LoginRequiredMixin, ListView):
    """Вывод списка получатеелй рассылки"""
    model = MailingClient
    template_name = 'client/сlient_list.html'
    paginate_by = 6


class ClientsDetailView(LoginRequiredMixin, DetailView):
    """Получение детальной информации по получателю рассылки"""
    model = MailingClient
    template_name = 'client/сlient_deteil.html'
    context_object_name = 'item'
    pk_url_kwarg = 'pk'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление получателя рассылки"""
    model = MailingClient
    permission_required = "client.delete_mailingclient"
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'
    template_name = 'client/delete_client.html'
    success_url = reverse_lazy('client:client_list')


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение данных получателя рассылки"""
    model = MailingClient
    form_class = ClientForm
    permission_required = "client.change_mailingclient"
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'
    template_name = 'client/update_form.html'

    def get_success_url(self) -> str:
        """Изменение url (заглушка)"""
        new_url = slugify(self.object.pk)
        return reverse('client:client_detail', args=[new_url])
