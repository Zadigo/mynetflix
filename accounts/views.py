import hashlib

from accounts import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http.response import (HttpResponseForbidden, HttpResponseNotFound,
                                  HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, View

from django.contrib.auth.forms import PasswordResetForm

USER_MODEL = get_user_model()


@method_decorator(sensitive_post_parameters('username', 'password'), 'dispatch')
@method_decorator(never_cache, 'dispatch')
class LoginView(FormView):
    """Login the user"""
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('accounts:login_view')

    def form_valid(self, form):
        # Use a conditional get on the cleaned_data
        # dict since one or the other might not be
        # present on the incoming data. Only one of
        # email and username is present on the form
        email = form.cleaned_data.get('email', None)
        username = form.cleaned_data.get('username', None)
        password = form.cleaned_data['password']
        if email is not None:
            user = authenticate(
                self.request, username=username, password=password)
            if user is not None:
                login(self.request, user)
                return redirect(reverse('home_view'))
            else:
                form.add_error(None, _("User does not exist"))
                return self.form_invalid(form)
        return super().form_valid(form)


class LogoutView(RedirectView):
    """Logout the user"""
    url = reverse_lazy('home_view')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(self.request)
        return super().get(request, *args, **kwargs)


class RedirectUrlMixin:
    """Class that handles page redirections
    after the user has signup notably for
    entering aditional profile information"""
    redirect_url = None
    # Sequentially go to each url
    redirect_urls = []
    flow_name = 'auth_flow'

    @staticmethod
    def hash(value):
        value = str(value)
        instance = hashlib.md5(str(value).encode("utf-8"))
        return instance.hexdigest()

    def compare(self, request, user):
        """Checks that the hashed email and id were
        found in the current session or at the very
        least, that the user can be found in the database"""
        result = []

        flow = request.get(self.flow_name, {})
        hashed_email = flow['email']
        hashed_id = flow['id']

        if flow:
            result.append(
                [
                    hashed_email == self.hash(user.email),
                    hashed_id == self.hash(user.id)
                ]
            )
        return any(result)

    def get_redirect_url(self):
        url = str(self.redirect_url)
        return HttpResponseRedirect(url)

    def set_user_for_redirect(self, user, request):
        # Set the hashed email address, save it to the
        # session, in the url and then use this to
        # recognize the user within the flow
        hashed_id = self.hash(user.id)
        hashed_email = self.hash(user.email)
        request.session[self.flow_name] = {
            'id': hashed_id,
            'email': hashed_email
        }
        return hashed_id, hashed_email

    def clean_user_from_redirect(self, request):
        request.session[self.flow_name] = None

    def get_user_for_redirect(self, hashed_email):
        inactive_users = USER_MODEL.objects.filter(is_active=False)
        if not inactive_users.exists():
            return False

        found_user = None

        for user in inactive_users:
            if self.hash(user.email) == hashed_email:
                found_user = user
                break

        if found_user is None:
            return False

        return found_user


@method_decorator(sensitive_post_parameters(), 'dispatch')
@method_decorator(never_cache, 'dispatch')
class SignupView(RedirectUrlMixin, FormView):
    """Signup the user"""
    template_name = 'signup.html'
    form_class = forms.SignupForm
    success_url = reverse_lazy('accounts:login_view')

    def get_redirect_url(self, token):
        self.redirect_url = reverse(
            'accounts:complete_account',
            token=token
        )
        return super().get_redirect_url()

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        credentials = {
            'username': username,
            'email': email,
            'password': password
        }
        queryset = USER_MODEL.objects.filter(
            email=email,
            username=username
        )
        if queryset.exists():
            form.add_error(None, _("User exists already"))
            return self.form_invalid(form)

        user = USER_MODEL.objects.create_user(**credentials)

        if self.redirect_url is not None:
            _, hased_email = self.set_user_for_redirect(user, self.request)
            return self.get_redirect_url(hased_email)
        return super().form_valid(form)


@method_decorator(sensitive_post_parameters('email'), 'dispatch')
@method_decorator(never_cache, 'dispatch')
class ForgotPasswordView(FormView):
    template_name = 'forgot_password.html'
    success_url = reverse_lazy('accounts:login')
    form_class = forms.ForgotPasswordForm

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)


class ActivateAccountView(View):
    pass


class AdditionalInformationView(RedirectUrlMixin, FormView):
    """User completes additional information for
    his profile"""
    template_name = 'additional_information.html'
    form_class = forms.AdditionalInformationForm
    success_url = reverse_lazy('accounts:home_view')

    def get(self, request, token, *args, **kwargs):
        user = self.get_user_for_redirect(token)
        if not user:
            pass

        if user.is_active:
            return HttpResponseForbidden('Completed')

        context = self.get_context_data(hashed_email=token)
        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.get_user_for_redirect(self.kwargs['token'])
        if not user:
            return HttpResponseNotFound('Not found')

        fields = ['lastname', 'firstname']
        for field in fields:
            setattr(user, field, form.cleaned_data[field])
        user.save()
        self.clean_user_from_redirect(self.request)
        return super().form_valid(form)
