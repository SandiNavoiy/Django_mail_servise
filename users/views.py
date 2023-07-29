import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils.encoding import force_str
from users.forms import UserForgotPasswordForm, UserSetNewPasswordForm
from users.forms import UserRegisterForm, UserUpdate
from users.models import User


class RegisterView(CreateView):
    """Регистрация"""
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """отправка ссылки"""
        user = form.save(commit=False)
        user.is_active = False  # User will be activated after email verification
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        activation_link = reverse_lazy(
            'users:email_verification', kwargs={'uidb64': uid})
        activation_url = f"{current_site}{activation_link}"
        mail_subject = 'Активируйте свой аккаунт'
        massage = render_to_string('users/email_verification.html', {
            'activation_url': activation_url
        })
        user.email_user(mail_subject, massage)

        return super().form_valid(form)


def activate_account(request, uidb64):
    """активация"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=int(uid))
        user.is_active = True
        user.save()
        return redirect('users:activation_ok')
    except User.DoesNotExist:
        return redirect('users:activation_failed')


class ActivationOk(TemplateView):
    """Активация успешна"""
    template_name = 'users/email_verification_done.html'


class ActivationFailed(TemplateView):
    """Активация не успешна"""
    template_name = 'users/email_verification_failed.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление юзера"""
    model = User
    form_class = UserUpdate
    template_name = "users/update_user.html"
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user


def gen_pass(request):
    """Генерация пароля https://proghunter.ru/articles/django-base-2023-password-recovery-form"""
    new_password = str(random.randint(1000, 9999))
    request.user.set_password(new_password)
    request.user.save()
    send_mail('Ваш пароль изменен',
              f"Ваш пароль: {new_password} обязательно поменяйте его", 'noreply@oscarbot.ru', [request.user.email])
    return redirect('mailing:index')


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('mailing:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('mailing:index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context
