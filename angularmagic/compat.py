import inspect

import django.db.models

try:
    import simplejson as json
except ImportError:
    import json

try:
    import rest_framework
    REST_FRAMEWORK = True
except ImportError:
    REST_FRAMEWORK = False


class BaseSerializer(object):

    def serialize(self, obj, *args, **kwargs):
        raise NotImplementedError


class BaseRenderer(object):

    def render(self, obj, *args, **kwargs):
        raise NotImplementedError


def is_serializer(SerializerClass):
    if inspect.isclass(SerializerClass):
        if issubclass(SerializerClass, BaseSerializer):
            return (True, None)

        if REST_FRAMEWORK:
            from rest_framework.serializers import Serializer, ModelSerializer

            if issubclass(SerializerClass, ModelSerializer):
                model = SerializerClass.Meta.model
            else:
                model = None

            return (issubclass(SerializerClass, Serializer), model)

    return (False, None)


def serializer_factory(obj):
    if isinstance(obj, django.db.models.Model):
        ModelClass = type(obj)
        serializer_name = ModelClass.__name__ + 'Serializer'

        if REST_FRAMEWORK:
            from rest_framework.serializers import ModelSerializer

            SerializerMeta = type('Meta', (), {'model': ModelClass})
            SerializerClass = type(serializer_name, (ModelSerializer,),
                                   dict(Meta=SerializerMeta))

    return None


def serialize(serializer_obj, data):
    if isinstance(serializer_obj, BaseSerializer):
        return serializer_obj.serialize(data)

    if REST_FRAMEWORK:
        from rest_framework.serializers import Serializer

        if isinstance(serializer_obj, Serializer):
            return serializer_obj.to_native(data)

    raise TypeError("Don't know how to use \"%s\" object as serializer",
                    type(serializer_obj).__name__)

def render(renderer_obj, data):
    if isinstance(renderer_obj, BaseRenderer):
        return renderer_obj.render(data)
    
    if isinstance(renderer_obj, json.JSONEncoder):
        return renderer_obj.encode(data)

