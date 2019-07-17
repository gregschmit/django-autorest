"""
This module implements a factory for dynamically generating ``ModelViewSet``s.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.utils.module_loading import import_string

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .settings import get_setting


class ModelViewSetFactory:
    """
    Factory for building ModelViewSet objects for models.
    """

    def __init__(self):
        # if we're using admin.py, figure out which admin site to use
        self.default_use_admin = get_setting('AUTOREST_DEFAULT_USE_ADMIN_SITE')
        self.admin_site = import_string(get_setting('AUTOREST_ADMIN_SITE'))
        self.config = get_setting('AUTOREST_CONFIG')

    def _get_cfg_s(self, key, config=None):
        """
        Return and convert (from string -> class) an item from config, or
        ``None``.
        """
        if not config: config = self.config
        if issubclass(type(config.get(key, None)), str):
            return import_string(config[key])
        return None

    def build(self, model_cls):
        """
        Build and return a viewset, allowing the config to dominate the default
        configuration.
        """
        model_cls = model_cls
        model = model_cls.__name__
        app = model_cls._meta.app_label
        model_config = self.config.get(app, {}).get(model, {})
        use_admin = model_config.get('use_admin_site', self.default_use_admin)

        if use_admin:
            serializer = self._get_cfg_s('serializer', model_config)
            viewset = self._get_cfg_s('viewset', model_config)
        else:
            serializer = viewset = None

        class DefaultModelSerializer(ModelSerializer):
            class Meta:
                model = model_cls
                fields = '__all__'

        class DefaultModelViewSet(ModelViewSet):
            model = model_cls
            queryset = model_cls.objects.all()
            serializer_class = serializer or DefaultModelSerializer
            filterset_fields = '__all__'

            def __init__(self, **kwargs):
                """
                Override the ``__class__.__name__`` so the
                ``ModelViewSet.get_view_name()`` builds the name in a sensible
                way, rather than calling every object "Default".
                """
                r = super().__init__(**kwargs)
                self.__class__.__name__ = f"{model}ViewSet"
                return r

        return viewset or DefaultModelViewSet


def intentionally_bad_api_view(request):
    """
    For development/testing purposes; renders invalid JSON.
    """
    return HttpResponse('{{"data": 5}')
