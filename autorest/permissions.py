"""
This module provides a custom verison of
``rest_framework.permissions.DjangoModelPermissions`` that adds the ``view``
permission.

TODO: should be removed when DRF Ticket #6324 is resolved (likely by PR #6325):
 - https://github.com/encode/django-rest-framework/issues/6324)
 - https://github.com/encode/django-rest-framework/pull/6325
"""

from rest_framework import permissions


class CustomModelPermissions(permissions.DjangoModelPermissions):
    """
    Similar to ``DjangoObjectPermissions``, but adding ``view`` permissions.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
