# from django.contrib import admin
from accounts.sites import custom_admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/v1/accounts/', include('accounts.api_urls')),
    path('api/v1/movies/', include('movies.api.urls')),
    path('api/v1/shows/', include('shows.api')),
    path('admin/', custom_admin_site.urls)
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
