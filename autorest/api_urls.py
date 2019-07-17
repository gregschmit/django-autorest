"""
This module builds the API URLs and hooks in the API ``ViewSet``s.
"""

from django.apps import apps
from rest_framework import routers

from .api_views import ModelViewSetFactory
from .url_inflect import url_deviations


print("AutoREST: building API resources for models:")
router = routers.SimpleRouter()
viewset_factory = ModelViewSetFactory()
for app in apps.get_app_configs():
    for model in app.get_models():
        viewset = viewset_factory.build(model)
        for model_url in url_deviations(model.__name__):
            url_pattern = "{}/{}".format(app.label, model_url)
            print("  {}".format(url_pattern))
            router.register(url_pattern, viewset)
        print(f"   {viewset}")
print('')
urlpatterns = router.urls
