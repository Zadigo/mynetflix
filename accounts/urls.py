from django.urls import re_path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    re_path(
        r'^forgot-password$',
        views.ForgotPasswordView.as_view(),
        name='forgot_password'
    ),
    re_path(
        r'^complete-information/(?P<token>[a-z0-9]+)$',
        views.AdditionalInformationView.as_view(),
        name='complete_account_view'
    ),
    re_path(r'^logout$', views.LogoutView.as_view(), name='logout_view'),
    re_path(r'^signup$', views.SignupView.as_view(), name='signup_view'),
    re_path(r'^login$', views.LoginView.as_view(), name='login')
]
