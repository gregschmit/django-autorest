"""
This module calls the ``ModelViewSetFactory`` to either get or build the
viewsets and then registers them to this module's ``urlpatterns`` to allow for
being included by other URL dispatchers.
"""

from django.apps import apps
from rest_framework import routers

from .views import ModelViewSetFactory
from .url_inflect import url_deviations
from ..settings import get_setting


def configure_router(router, silent=False, **kwargs):
    p = lambda *args, **kwargs: print(*args, **kwargs) if not silent else None
    p("AutoREST: building API resources for models:")

    # collect settings, overridable by kwargs
    api_settings = {}
    for s in ["default_enable", "default_use_admin_site", "admin_site", "config"]:
        api_settings[s] = kwargs.get(s, get_setting("AUTOREST_{}".format(s.upper())))

    # build API
    viewset_factory = ModelViewSetFactory(**api_settings)
    for app in apps.get_app_configs():
        for model in app.get_models():
            viewset = viewset_factory.build(model)
            if not viewset:
                continue
            p(f"  ViewSet: {viewset.__module__}.{viewset.__name__}")
            for model_url in url_deviations(model.__name__):
                url_pattern = "{}/{}".format(app.label, model_url)
                p("    {}".format(url_pattern))
                router.register(url_pattern, viewset)
    p("")
    return router


api_router = configure_router(routers.DefaultRouter())
urlpatterns = api_router.urls
