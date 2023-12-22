from django.contrib import admin

from movies import models
from accounts.admin import custom_admin_site


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'duration', 'genre']
    search_fields = ['title', 'plot', 'actors__firstname', 'actors__lastname']


class DirectorAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']


class ActorAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']


class WriterAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'firstname', 'lastname']
    search_fields = ['firstname', 'lastname']


custom_admin_site.register(models.Movie, MovieAdmin)
custom_admin_site.register(models.Actor, ActorAdmin)
custom_admin_site.register(models.Director, DirectorAdmin)
custom_admin_site.register(models.Writer, WriterAdmin)
