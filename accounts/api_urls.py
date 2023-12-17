from accounts import api_views
from django.urls import re_path

app_name = 'accounts'

urlpatterns = [
    re_path(r'profile$', api_views.profile, name='api_profile'),
    re_path(
        r'forgot-password$',
        api_views.forgot_password,
        name='api_forgot_password'
    ),
    re_path(
        r'reset-password/(?P<token>\d+)$',
        api_views.reset_password,
        name='api_reset_password'
    ),
    re_path(r'logout$', api_views.logout, name='api_logout'),
    re_path(r'signup$', api_views.signup, name='api_signup'),
    re_path(r'login$', api_views.login, name='api_login')
]
