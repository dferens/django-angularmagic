try:
    import simplejson as json
except ImportError:
    import json
try:
    import rest_framework
except ImportError:
    rest_framework = False

import django.db.models

from . import base


if rest_framework:
    class RestFrameworkSerializerAdapter(base.Serializer):

        def __init__(self, SerializerClass, obj):
            super(RestFrameworkSerializerAdapter, self).__init__(obj)
            self.SerializerClass = SerializerClass
            self.model = SerializerClass.Meta.model
            self.obj = obj

        def serialize(self):
            many = hasattr(self.obj, '__iter__')
            return self.SerializerClass(self.obj, many=many).data


def create_serializer_adapter(SerializerClass, obj):
    """
    :return: ``angularmagic.base.Serializer`` instance.
    """
    if rest_framework:
        from rest_framework.serializers import Serializer

        if issubclass(SerializerClass, Serializer):
            return RestFrameworkSerializerAdapter(SerializerClass, obj)

    raise TypeError('Unknown serializer class: %s' % SerializerClass.__name__)

