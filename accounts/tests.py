from django.test import TestCase
from django.test.client import RequestFactory, Client
from accounts import views
from accounts import api_views
from django.urls import reverse
from django.http.response import HttpResponse


class TestLoginView(TestCase):
    def test_can_get_view(self):
        factory = RequestFactory()
        request = factory.get(reverse('accounts:login_view'))
        view = views.LoginView()
        view.setup(request)

        response = view.get(request)

        self.assertEqual(response.status_code, 200)

    def test_can_post_view(self):
        factory = RequestFactory()
        request = factory.post(reverse('accounts:login_view'))
        view = views.LoginView()
        view.setup(request)

        response = view.get(request)

        self.assertEqual(response.status_code, 200)


class TestSignupView(TestCase):
    def test_can_signup(self):
        client = Client()
        response = client.post(
            reverse('accounts:signup_view'),
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': 'This-is-a-valid-password',
                'password2': 'This-is-a-valid-password'
            }
        )

        # form = response['form']
        # Test that the signup form does not return
        # any kinds of errors: length, capital letter
        # self.assertFalse(form.has_error('password1'))
        # self.assertEqual(response.status_code, 200)


class TestAPIViews(TestCase):
    fixtures = ['users']
    
    def setup(self):
        self.factory = RequestFactory()

    def login_view(self):
        request = self.factory.get(reverse('accounts:api_login'))
        response = api_views.login(request)
        self.assertEqual(response.status_code, 200)

    def signup_view(self):
        request = self.factory.get(reverse('accounts:api_sigup'))
        response = api_views.login(request)
        self.assertEqual(response.status_code, 200)

    def logout_view(self):
        request = self.factory.get(reverse('accounts:logout'))
        response = api_views.login(request)
        self.assertEqual(response.status_code, 200)
