"""
This module calls the ``ModelViewSetFactory`` to either get or build the
viewsets and then registers them to this module's ``urlpatterns`` to allow for
being included by other URL dispatchers.
"""

from rest_framework import routers

from .views import configure_router


api_router = configure_router(routers.DefaultRouter(), print_out=True)
urlpatterns = api_router.urls
