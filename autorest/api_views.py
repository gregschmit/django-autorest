"""
This module implements a factory for dynamically generating ``ModelViewSet``s.
"""

from django.utils.module_loading import import_string

from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.viewsets import ModelViewSet

from .settings import get_setting


# the first entry in each list should be the DRF action name.
ACTION_SYNONYMS = [
    ['create', 'add'],
    ['retrieve', 'detail'],
    ['destroy', 'delete'],
]


def _get_synonyms(word):
    """
    Get synonyms for this word, or a list with this word in it only.
    """
    for group in ACTION_SYNONYMS:
        if word in group: return group
    return [word]


def _action(word):
    """
    Return the DRF action keyword for a given word, if there exists one, else
    return the word unchanged.
    """
    return _get_synonyms(word)[0]


class ModelSerializerFactory:
    """
    Factory for building ``ModelSerializer`` objects for models.
    """

    def __init__(self, app, model):
        self.app = app
        self.model = model

    def build(self, stype='Default', fields='__all__', write_only_fields=None):
        """
        Build a custom ``ModelSerializer``
        """
        meta = {
            'model': self.model,
            'fields': fields,
        }
        hard_fields = {}
        if write_only_fields:
            for f in write_only_fields:
                # remove from normal fields
                # try:
                #     fields.remove(f)
                # except ValueError:
                #     pass
                # add CharField
                cf = CharField(write_only=True)
                hard_fields[f] = cf
            #extra = {k: {'write_only': True} for k in write_only_fields}
            #meta['extra_kwargs'] = extra
        cms_meta = type('Meta', (object,), {**meta})
        cms = type(
            f"{self.app.title()}{self.model.__name__}{stype}Serializer",
            (ModelSerializer,),
            {'Meta': cms_meta, **hard_fields},
        )
        return cms


class ModelViewSetFactory:
    """
    Factory for building ``ModelViewSet`` objects for models.
    """

    def __init__(self):
        self.default_use_admin = get_setting('AUTOREST_DEFAULT_USE_ADMIN_SITE')
        self.admin_site = import_string(get_setting('AUTOREST_ADMIN_SITE'))
        self.config = get_setting('AUTOREST_CONFIG')

    def _get_cfg_s(self, key, config=None):
        """
        Return, and convert from string, an item from config, or ``None``.
        """
        if not config: config = self.config
        if isinstance(config.get(key, None), str):
            return import_string(config[key])
        return None

    def _get_serializer(self, name, app, model, model_cfg):
        # check to see if we're using admin
        use_admin = model_cfg.get('use_admin_site', self.default_use_admin)

        # prepare the Factory
        msf = ModelSerializerFactory(app, model)

        # return early if we cannot build
        if not (use_admin and self.admin_site and model in self.admin_site._registry):
            if name == 'default':
                # we must return a serializer for default
                return msf.build()
            return None

        # get the model admin
        admin = self.admin_site._registry[model]

        # try to build the serializer by type
        serializer = None
        pk_field = model._meta.pk.name
        if name == 'list':
            if hasattr(admin, 'list_display') and admin.list_display:
                pk = []
                if not pk_field in admin.list_display:
                    pk.append(pk_field)
                serializer = msf.build('List', [*pk, *admin.list_display])
        elif name == 'create':
            if hasattr(admin, 'add_fieldsets') and admin.add_fieldsets:
                f = []
                [f.extend(y.get('fields', [])) for x,y in admin.add_fieldsets]
                serializer = msf.build('Create', f, f)
            elif hasattr(admin, 'fields') and admin.fields:
                serializer = msf.build('Create', admin.fields)
        else:
            if hasattr(admin, 'fieldsets') and admin.fieldsets:
                f = []
                [f.extend(y.get('fields', [])) for x,y in admin.fieldsets]
                pk = []
                if not pk_field in f:
                    pk.append(pk_field)
                serializer = msf.build('CustomDefault', [*pk, *f])
            elif hasattr(admin, 'fields') and admin.fields:
                pk = []
                if not pk_field in f:
                    pk.append(pk_field)
                serializer = msf.build('CustomDefault', [*pk, *admin.fields])

        # again, we must provide a serializer for default
        if not serializer and name == 'default':
            serializer = msf.build()

        return serializer

    def build(self, model):
        """
        Build and return a viewset, allowing the config to dominate the default
        configuration.
        """
        model_name = model.__name__
        app = model._meta.app_label
        model_cfg = self.config.get(app, {}).get(model_name, {})

        # check if we should be processing this model
        if not get_setting('AUTOREST_DEFAULT_ENABLE') and not model_cfg:
            return False

        # check if we already have a viewset
        viewset = self._get_cfg_s('viewset', model_cfg)
        if viewset: return viewset

        # We need to eventually fill in these serializers (or at least default):
        actions = ['default', 'create', 'list', 'retrieve', 'update']
        serializers = {k:None for k in actions}

        # try to retrieve configured serializers
        serializers['default'] = self._get_cfg_s('serializer', model_cfg)
        for name, _ in serializers.items():
            synonyms = _get_synonyms(name)
            for action in synonyms:
                s = self._get_cfg_s(f'{action}_serializer', model_cfg)
                if s:
                    serializers[name] = s
                    break

        # if we don't have a default serializer, then build!
        if not serializers['default']:
            for name in [k for k,v in serializers.items() if not v]:
                serializers[name] = self._get_serializer(name, app, model, model_cfg)

        # build the viewset get_serializer_class method
        def get_serializer_class(self):
            try:
                s = self.action_serializers[self.action]
                if s: return s
            except KeyError:
                pass
            return self.action_serializers['default']

        # build the viewset
        mvs = type(f"{app.title()}{model_name}ViewSet", (ModelViewSet,), {
            'model': model,
            'queryset': model.objects.all(),
            'filterset_fields': '__all__',
            'action_serializers': serializers,
            'get_serializer_class': get_serializer_class,
        })

        return mvs
