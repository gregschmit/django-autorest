"""
This module builds the API URLs and hooks in the API ``ViewSet``s.
"""

from django.apps import apps
from rest_framework import routers

from .api_views import ModelViewSetFactory
from .settings import get_setting
from .api_url_inflect import url_deviations


print("AutoREST: building API resources for models:")
router = routers.SimpleRouter()
viewset_factory = ModelViewSetFactory()
for app in apps.get_app_configs():
    for model in app.get_models():
        viewset = viewset_factory.build(model)
        if not viewset: continue
        print(f"  ViewSet: {viewset.__module__}.{viewset.__name__}")
        if hasattr(viewset, 'action_serializers'):
            print("    action_serializers: {")
            for action,serializer in viewset.action_serializers.items():
                if serializer:
                    print("      {}: {}.{} :: {},".format(
                        action,
                        serializer.__module__,
                        serializer.__name__,
                        serializer.Meta.fields,
                    ))
            print("    }")
        for model_url in url_deviations(model.__name__):
            url_pattern = "{}/{}".format(app.label, model_url)
            print("    {}".format(url_pattern))
            router.register(url_pattern, viewset)
print('')
urlpatterns = router.urls
