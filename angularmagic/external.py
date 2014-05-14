try:
    import simplejson as json
except ImportError:
    import json
try:
    import rest_framework
except ImportError:
    rest_framework = False
try:
    import tastypie
except ImportError:
    tastypie = False

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


if tastypie:
    class TastypieSerializerAdapter(base.Serializer):

        def __init__(self, ResourceClass, obj):
            super(TastypieSerializerAdapter, self).__init__(obj)
            self.resource = ResourceClass()
            self.model = ResourceClass._meta.queryset.model
            self.obj = obj

        def serialize(self):
            if hasattr(self.obj, '__iter__'):
                def serialize_obj(obj):
                    bundle = self.resource.build_bundle(obj=obj)
                    self.resource.full_dehydrate(bundle, for_list=True)
                    return bundle.data

                return [serialize_obj(obj) for obj in self.obj]
            else:
                bundle = self.resource.build_bundle(obj=self.obj)
                self.resource.full_dehydrate(bundle)
                return bundle.data


def create_serializer_adapter(SerializerClass, obj):
    """
    :return: ``angularmagic.base.Serializer`` instance.
    """
    if rest_framework:
        from rest_framework.serializers import Serializer

        if issubclass(SerializerClass, Serializer):
            return RestFrameworkSerializerAdapter(SerializerClass, obj)

    if tastypie:
        from tastypie.resources import Resource

        if issubclass(SerializerClass, Resource):
            return TastypieSerializerAdapter(SerializerClass, obj)

    raise TypeError('Unknown serializer class: %s' % SerializerClass.__name__)

