from django.apps import apps
from django.contrib.admin import site
from django.http import HttpResponse, HttpResponseNotFound
from django.views import generic, View
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView


class CustomModelViewSetFactory:
    """
    Factory for building ModelViewSet objects for models.
    """

    @classmethod
    def build(cls, model_class):
        class CustomModelSerializer(ModelSerializer):

            class Meta:
                model = model_class
                fields = '__all__'

        class CustomModelViewSet(ModelViewSet):
            model = model_class
            queryset = model_class.objects.all()
            serializer_class = CustomModelSerializer
            filterset_fields = '__all__'

            def __init__(self, **kwargs):
                r = super().__init__(**kwargs)
                self.name = self.model.__name__ + " ViewSet"
                return r

        return CustomModelViewSet


def intentionally_bad_api_view(request):
    """
    For testing purposes; renders invalid JSON.
    """
    return HttpResponse('{{"blah": 5}')
