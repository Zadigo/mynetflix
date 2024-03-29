from accounts import forms
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    login_form = forms.CustomAdminAuthenticationForm


# Create a custom admin which allows authenticating
# with the custom created email authentication model
custom_admin_site = CustomAdminSite(name='Custom Admin')
