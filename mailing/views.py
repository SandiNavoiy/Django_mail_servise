from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, ListView, UpdateView
from blog.models import BlogPost
from client.models import MailingClient
from config import settings
from mailing.forms import SettingsForm, MailForm
from mailing.models import Mail, MailingSettings, MailingTry


class Home(TemplateView):
    '''Домашняя страница'''
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        """Переопределяем вывод конкретных данынх в шаблон"""
        context = {}
        mails = Mail.objects.all().count()
        active = MailingSettings.objects.filter(mailing_status='AC').values_list().count(),
        clients = MailingClient.objects.all().count()
        random_article = BlogPost.objects.order_by('?')[:3]
        context['mails'] = mails
        context['active'] = active[0]
        context['clients'] = clients
        context['random_article'] = random_article
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания рассылки"""
    template_name = "mailing/mail_form.html"
    model = MailingSettings
    form_class = SettingsForm
    success_url = reverse_lazy('mailing:mailing_list')
    mail_data = ''
    mail_status = 'OK'

    def get_context_data(self, **kwargs):
        '''Функция получения контекстных данных и создания подформы с сообщением'''
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(MailingSettings, Mail, form=MailForm, can_delete=False,
                                            extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST or None, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        '''Функция для валидации формы, получения данных и их обработки'''
        data = self.get_context_data()
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        formset = data['formset']
        client_email = []
        mailing_subject = ''
        mailing_body = ''
        for fo in formset:
            if fo.is_valid():
                clients = fo.cleaned_data.get('client_to_message').values_list()
                for i in clients:
                    client_email.append(i[2])
                mailing_subject = fo.cleaned_data.get('mailing_subject')
                mailing_body = fo.cleaned_data.get('mailing_body')
                all_clients = fo.cleaned_data.get('all_clients')
                if all_clients:
                    client_email = list(MailingClient.objects.all().values_list('contact_email', flat=True))
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.mailing_status = "AC"
            mailing.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.author = self.request.user
            formset.save()
        self.object.save()
        ct = datetime.now()
        '''Тут сверяется время рассылки и если она истекла, то она отключается'''
        try:
            if self.object.mailing_time_start.timestamp() <= ct.timestamp() <= self.object.mailing_time_end.timestamp():
                sending = send_mail(mailing_subject, mailing_body, settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=client_email,
                                    fail_silently=False)
                if sending == 1:
                    self.mail_status = 'OK'
                else:
                    self.mail_status = 'Не отправлено'

            if (self.object.mailing_periods == "DL") and ((
                                                                  self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=1)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "WL") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=6)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "ML") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=30)):
                self.object.mailing_status = 'FI'
                self.object.save()

            MailingTry.objects.create(mailing=self.object, mailing_try=datetime.now(),
                                      mailing_try_status=self.object.mailing_status,
                                      mailing_response=self.mail_status)
            return super().form_valid(form)
        except AttributeError:
            form.add_error(None, 'Установите дату рассылки.')
            return super(MailingCreateView, self).form_invalid(form)


class MailingListView(LoginRequiredMixin, ListView):
    '''Контроллер списка рассылок'''
    template_name = "mailing/mailing_list.html"
    model = Mail
    paginate_by = 10
    extra_context = {
        'title': 'Мои рассылки'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.status_type == 'MANAGER':
            raise PermissionDenied
        return self.object

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    '''Удаление  рассылки'''
    model = Mail
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy('mailing:mailing_list')

    def delete(self, request, *args, **kwargs):
        # Получаем объект рассылки
        self.object = self.get_object()
        # Удаляем рассылку
        self.object.delete()
        messages.success(request, 'Рассылка успешно удалена.')
        return redirect(self.success_url)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер для изменения рассылки. '''
    template_name = "mailing/mail_form_update.html"
    model = MailingSettings
    form_class = SettingsForm
    success_url = reverse_lazy('mailing:mailing_list')
    mail_data = ''
    mail_status = 'OK'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user:
            raise PermissionDenied
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(MailingSettings, Mail, form=MailForm, can_delete=False,
                                            extra=0, edit_only=True)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST or None, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        data = self.get_context_data()
        self.object = form.save()
        formset = data['formset']
        client_email = []
        mailing_subject = ''
        mailing_body = ''
        for fo in formset:
            if fo.is_valid():
                clients = fo.cleaned_data.get('client_to_message').values_list()
                for i in clients:
                    client_email.append(i[2])
                mailing_subject = fo.cleaned_data.get('mailing_subject')
                mailing_body = fo.cleaned_data.get('mailing_body')
                all_clients = fo.cleaned_data.get('all_clients')
                if all_clients:
                    client_email = list(MailingClient.objects.all().values_list('contact_email', flat=True))
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.mailing_status = "AC"
            mailing.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        self.object.save()
        ct = datetime.now()  # текущая дата/время

        try:
            if self.object.mailing_time_start.timestamp() <= ct.timestamp() <= self.object.mailing_time_end.timestamp():
                sending = send_mail(mailing_subject, mailing_body, settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[client_email],
                                    fail_silently=False)
                if sending == 1:
                    self.mail_status = 'OK'
                else:
                    self.mail_status = 'Не отправлено'

            if (self.object.mailing_periods == "DL") and ((
                                                                  self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=1)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "WL") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=6)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "ML") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=30)):
                self.object.mailing_status = 'FI'
                self.object.save()

            MailingTry.objects.create(mailing=self.object, mailing_try=datetime.now(),
                                      mailing_try_status=self.object.mailing_status,
                                      mailing_response=self.mail_status)
            return super().form_valid(form)
        except AttributeError:
            form.add_error(None, 'Установите дату рассылки.')
            return super(MailingUpdateView, self).form_invalid(form)


class MailingTryListView(LoginRequiredMixin, ListView):
    '''Статистика по отправкам'''
    template_name = "mailing/log_view.html"
    model = MailingTry
    paginate_by = 10
    extra_context = {
        'title': 'Отчет по рассылкам'
    }
