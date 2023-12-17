from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AuthenticationSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        return [
            'accounts:login_view',
            'accounts:signup_view',
            'accounts:forgot_password_view'
        ]

    def location(self, item):
        return reverse(item)
