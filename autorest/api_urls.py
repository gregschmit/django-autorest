"""
This module calls the ``ModelViewSetFactory`` to either get or build the
viewsets and then registers them to this module's ``urlpatterns`` to allow for
being included by other URL dispatchers.
"""

from django.apps import apps
from rest_framework import routers

from .api_views import ModelViewSetFactory
from .api_url_inflect import url_deviations


print("AutoREST: building API resources for models:")
router = routers.DefaultRouter()
viewset_factory = ModelViewSetFactory()
for app in apps.get_app_configs():
    for model in app.get_models():
        viewset = viewset_factory.build(model)
        if not viewset: continue
        print(f"  ViewSet: {viewset.__module__}.{viewset.__name__}")
        for model_url in url_deviations(model.__name__):
            url_pattern = "{}/{}".format(app.label, model_url)
            print("    {}".format(url_pattern))
            router.register(url_pattern, viewset)
print('')
urlpatterns = router.urls
