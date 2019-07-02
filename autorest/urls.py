from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('autorest.api_urls')),
    path('admin/', admin.site.urls),
]
