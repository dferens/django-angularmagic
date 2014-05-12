try:
    import simplejson as json
except ImportError:
    import json

import django.db.models

try:
    import rest_framework
except ImportError:
    REST_FRAMEWORK = False
else:
    REST_FRAMEWORK = True


class BaseSerializer(object):

    @classmethod
    def get_model(cls):
        return None

    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)

    def serialize(self):
        raise NotImplementedError    


class BaseRenderer(object):

    def render(self):
        raise NotImplementedError


def create_serializer_class(ObjectClass):
    if issubclass(ObjectClass, django.db.models.Model):
        if REST_FRAMEWORK:
            from rest_framework.serializers import ModelSerializer

            SerializerMetaClass = type('Meta', (object,), {'model': ObjectClass})
            return type(ObjectClass.__name__ + 'Serializer',
                        (ModelSerializer,),
                        {'Meta': SerializerMetaClass})


def create_serializer(SerializerClass, obj):
    if issubclass(SerializerClass, BaseSerializer):
        return SerializerClass(obj)

    if REST_FRAMEWORK:
        from rest_framework.serializers import Serializer

        if issubclass(SerializerClass, Serializer):
            if hasattr(obj, '__iter__'):
                return SerializerClass(obj, many=True)
            else:
                return SerializerClass(obj)


def serialize(serializer_obj):
    if isinstance(serializer_obj, BaseSerializer):
        return serializer_obj.serialize()

    if REST_FRAMEWORK:
        from rest_framework.serializers import Serializer

        if isinstance(serializer_obj, Serializer):
            return serializer_obj.data


def get_serializer_model(SerializerClass):
    if issubclass(SerializerClass, BaseSerializer):
        return SerializerClass.get_model()

    if REST_FRAMEWORK:
        from rest_framework.serializers import ModelSerializer

        if issubclass(SerializerClass, ModelSerializer):
            return SerializerClass.Meta.model


def create_renderer(RendererClass, context):
    if issubclass(RendererClass, json.JSONEncoder):
        return RendererClass()    


def render(renderer_obj, context):
    if isinstance(renderer_obj, BaseRenderer):
        return renderer_obj.render()

    if isinstance(renderer_obj, json.JSONEncoder):
        return renderer_obj.encode(context)
