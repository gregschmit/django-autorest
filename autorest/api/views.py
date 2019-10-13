"""
This module implements a factory for dynamically generating ``ModelViewSet``s.
"""

from django.utils.module_loading import import_string

from action_serializer import ModelActionSerializer
from rest_framework.serializers import CharField
from rest_framework.viewsets import ModelViewSet


class ModelSerializerFactory:
    """
    Factory for building ``ModelActionSerializer`` objects for models.
    """

    def __init__(self, app, model):
        self.app = app
        self.model = model

    def build(self, fields="__all__", write_only_fields=None, action_fields={}):
        """
        Build a custom ``ModelActionSerializer``.
        """
        meta = {"model": self.model, "fields": fields, "action_fields": action_fields}
        hard_fields = {}
        if write_only_fields:
            for f in write_only_fields:
                cf = CharField(write_only=True)
                hard_fields[f] = cf
        cms_meta = type("Meta", (object,), {**meta})
        cms = type(
            f"{self.app.title()}{self.model.__name__}Serializer",
            (ModelActionSerializer,),
            {"Meta": cms_meta, **hard_fields},
        )
        return cms


class ModelViewSetFactory:
    """
    Factory for building ``ModelViewSet`` objects for models.
    """

    def __init__(self, default_enable, default_use_admin_site, admin_site, config):
        self.default_enable = default_enable
        self.default_use_admin_site = default_use_admin_site
        if isinstance(admin_site, str):
            admin_site = import_string(admin_site)
        self.admin_site = admin_site
        self.config = config

    def _get_cfg_s(self, key, config=None):
        """
        Return, and convert from string, an item from config, or ``None``.
        """
        if not config:
            config = self.config
        if isinstance(config.get(key, None), str):
            return import_string(config[key])
        return None

    def _get_serializer(self, app, model, model_cfg):
        # check to see if we're using admin
        use_admin = model_cfg.get("use_admin_site", self.default_use_admin_site)

        # prepare the Factory
        msf = ModelSerializerFactory(app, model)

        # return early if we cannot build
        if not (use_admin and self.admin_site and model in self.admin_site._registry):
            return msf.build()

        # get the model admin
        admin = self.admin_site._registry[model]

        # build actions if the right admin properties are defined
        action_fields = {}
        pk_field = model._meta.pk.name
        if hasattr(admin, "list_display") and admin.list_display:
            action_fields["list"] = {}
            action_fields["list"]["fields"] = []
            if not pk_field in admin.list_display:
                action_fields["list"]["fields"].append(pk_field)
            action_fields["list"]["fields"].extend(admin.list_display)
        if hasattr(admin, "add_fieldsets") and admin.add_fieldsets:
            action_fields["create"] = {}
            action_fields["create"]["fields"] = []
            [
                action_fields["create"]["fields"].extend(y.get("fields", []))
                for _, y in admin.add_fieldsets
            ]
        elif hasattr(admin, "fieldsets") and admin.fieldsets:
            action_fields["create"] = {}
            action_fields["create"]["fields"] = []
            action_fields["update"] = {}
            action_fields["update"]["fields"] = []
            for _, group in admin.add_fieldsets:
                f = group.get("fields", [])
                action_fields["create"]["fields"].extend(f)
                action_fields["update"]["fields"].extend(f)
        elif hasattr(admin, "fields") and admin.fields:
            action_fields["create"] = {}
            action_fields["create"]["fields"] = []
            action_fields["update"] = {}
            action_fields["update"]["fields"] = []
            action_fields["create"]["fields"].extend(admin.fields)
            action_fields["update"]["fields"].extend(admin.fields)

        return msf.build(action_fields=action_fields)

    def build(self, model):
        """
        Build and return a viewset, allowing the config to dominate the default
        configuration.
        """
        model_name = model.__name__
        app = model._meta.app_label
        model_cfg = self.config.get(app, {}).get(model_name, {})

        # check if we should be processing this model
        if not self.default_enable and not model_cfg:
            return False

        # check if we already have a viewset
        viewset = self._get_cfg_s("viewset", model_cfg)
        if viewset:
            return viewset

        # try to retrieve configured serializer
        serializer = self._get_cfg_s("serializer", model_cfg)

        # if we don't have a serializer, then build!
        if not serializer:
            serializer = self._get_serializer(app, model, model_cfg)

        # build the viewset
        mvs = type(
            f"{app.title()}{model_name}ViewSet",
            (ModelViewSet,),
            {
                "model": model,
                "queryset": model.objects.all(),
                "filterset_fields": "__all__",
                "serializer_class": serializer,
            },
        )

        return mvs
