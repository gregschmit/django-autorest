from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("api/", include("autorest.api_urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
