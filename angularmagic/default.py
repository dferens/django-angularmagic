import datetime

import django.db.models

from . import base
from .external import json


class Renderer(base.Renderer):

    render_rules = {
        datetime.date: lambda d: d.isoformat(),
        datetime.time: lambda t: t.isoformat(),
        datetime.datetime: lambda d: d.isoformat(),
        datetime.timedelta: lambda td: td.isoformat(),
    }

    format = 'json'

    def __init__(self, data):
        self.data = data

    def __jsonencoder_default(self, obj):
        module, name = type(obj).__module__, type(obj).__name__
        render_rule = self.render_rules.get(type(obj))
        return {'value': (render_rule or str)(obj),
                'py/object': '%s.%s' % (module, name)}

    def render(self):
        encoder = json.JSONEncoder(separators=(',', ':'),
                                   default=self.__jsonencoder_default)
        return encoder.encode(self.data)


class Serializer(base.Serializer):

    def __init__(self, obj):
        self.obj = obj

    def _serialize_model_instance(self, obj):
        """
        :param obj: ``django.db.models.Model`` instance
        """
        return {f.name: f.value_from_object(obj) \
                for f in type(obj)._meta.fields}

    def serialize(self):
        if hasattr(self.obj, '__iter__'):
            if len(self.obj):
                ObjectClass = type(self.obj[0])
                many = True
            else:
                return []
        else:
            ObjectClass, many = type(self.obj), False

        if issubclass(ObjectClass, django.db.models.Model):
            if many:
                return [self._serialize_model_instance(o) for o in self.obj]
            else:
                return self._serialize_model_instance(self.obj)
        else:
            return self.obj

