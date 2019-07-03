from django.apps import apps
from rest_framework import routers
from .api_views import CustomModelViewSetFactory
from .url_str import url_deviations


router = routers.SimpleRouter()
print("AutoREST: building API resources for models:")
for app in apps.get_app_configs():
    for model in app.get_models():
        vs = CustomModelViewSetFactory.build(model)
        for d in sorted(list(url_deviations(model.__name__))):
            p = "{0}/{1}".format(app.label, d)
            print("  {}".format(p))
            router.register(p, vs)
print('')
urlpatterns = router.urls
