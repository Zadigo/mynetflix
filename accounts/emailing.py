from accounts.models import CustomUser
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import exceptions
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _


class AuthenticationEmails:
    """A handler for sending
    authentication emails"""
    subject = None
    text_page = None
    html_page = None

    def __init__(self, request, email):
        self.email = email
        self.request = request
        self.user_cache = None
        self.use_https = False

    def get_context(self, domain_override=None, **extra_context):
        if domain_override is None:
            current_site = get_current_site(self.request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        context = {
            'email': self.email,
            'site_name': site_name,
            'domain': domain,
            'user': self.user_cache,
            'protocol': 'https' if self.use_https else 'http'
        }
        return context | extra_context
    
    def render_templates(self, **context):
        context = self.get_context()
        self.text = render_to_string(self.text_page, context)
        self.html = render_to_string(self.html_page, context)

    def send(self, **context):
        text, html = self.render_templates(**context)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        send_mail(
            self.subject,
            message=text,
            from_email=from_email,
            recipient_list=[self.email],
            fail_silently=True,
            html_message=html
        )


class LoginEmail(AuthenticationEmails):
    """Send an email when the user
    has logged into his account"""
    subject = _('Login from xxx')
    text_page = 'emails/login.txt'
    html_page = 'emails/login.html'


class SignupEmail(AuthenticationEmails):
    """Send an email when the user
    has newly signedup"""
    subject = _('Signup from xxx')
    text_page = 'emails/signup.txt'
    html_page = 'emails/signup.html'


class ForgotPasswordEmail(AuthenticationEmails):
    subject = _('Reset password')
    text_page = 'emails/forgot.txt'
    html_page = 'emails/forgot.html'

    def __init__(self, request, email, **context):
        super().__init__(request, email, **context)
        queryset = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True
        )
        if not queryset.exists():
            raise exceptions.BadRequest()
        self.user_cache = queryset.get()
        if not self.user_cache.has_usable_password():
            raise exceptions.BadRequest()

    def get_context(self, **context):
        context = super().get_context(**context)
        context['uid'] = urlsafe_base64_encode(force_bytes(self.user_cache.pk))
        context['token'] = default_token_generator.make_token(self.user_cache)
        return context
