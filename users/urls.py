from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, activate_account, ActivationOk, ActivationFailed, gen_pass, \
    UserForgotPasswordView, UserPasswordResetConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:uidb64>/', activate_account, name='email_verification'),
    path('success', ActivationOk.as_view(), name='activation_ok'),
    path('failed', ActivationFailed.as_view(), name='activation_failed'),
    path("gen_pass/", gen_pass, name="gen_pass"),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
