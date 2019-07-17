"""
This module implements a factory for dynamically generating ``ModelViewSet``s.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.utils.module_loading import import_string

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .settings import get_setting


class ModelSerializerFactory:

    def __init__(self, app, model):
        self.app = app
        self.model = model

    def build(self, stype, fields='__all__'):
        """
        Build a custom ``ModelSerializer``
        """
        cms_meta = type('Meta', (object,), {
            'model': self.model,
            'fields': fields,
        })
        cms = type(
            f"{self.app.title()}{self.model.__name__}{stype.title()}Serializer",
            (ModelSerializer,),
            {'Meta': cms_meta,},
        )
        return cms

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

        # check if we already have a viewset
        viewset = self._get_cfg_s('viewset', model_config)
        if viewset: return viewset

        # We need to eventually fill in these serializers:
        serializer = self._get_cfg_s('serializer', model_config)
        list_serializer = self._get_cfg_s('list_serializer', model_config)

        if not serializer or not list_serializer:
            # check to see if we're using admin
            use_admin = model_config.get('use_admin_site', self.default_use_admin)

            # prepare the Factory
            msf = ModelSerializerFactory(app, model_cls)

            if use_admin and self.admin_site and self.admin_site._registry[model_cls]:
                modeladmin = self.admin_site._registry[model_cls]

                # try to build list_serializer
                list_display = modeladmin.list_display
                if list_display:
                    list_serializer = msf.build('List', list_display)

                # try to build default serializer
                fields = modeladmin.fields or []
                if modeladmin.fieldsets:
                    f = []
                    [f.extend(y.get('fields', [])) for x,y in modeladmin.fieldsets]
                    if f:
                        [fields.append(x) for x in f if x not in fields]
                if fields:
                    serializer = msf.build('Default', fields)

            # if no serializer, use default:
            if not serializer:
                serializer = msf.build('Default')

            # last resort: use serializer as list serializer
            if not list_serializer:
                list_serializer = serializer

        def mvs__str__(self):
            return f"{model}ViewSet"

        def mvs_get_serializer_class(self):
            try:
                return self.action_serializers[self.action]
            except KeyError:
                pass
            return self.action_serializers['default']
        mvs = type(f"{app.title()}{model}ViewSet", (ModelViewSet,), {
            'model': model_cls,
            'queryset': model_cls.objects.all(),
            'filterset_fields': '__all__',
            'action_serializers': {  # must have default
                'list': list_serializer,
                'default': serializer,
            },
            'get_serializer_class': mvs_get_serializer_class,
        })

        return mvs


def intentionally_bad_api_view(request):
    """
    For development/testing purposes; renders invalid JSON.
    """
    return HttpResponse('{{"data": 5}')
