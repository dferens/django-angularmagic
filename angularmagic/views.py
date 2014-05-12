from django.conf import settings
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils import six

from . import appsettings, compat


class SerializerProviderMixin(object):

    serializer_classes = []

    def get_serializer_class(self, obj):
        ObjectClass = obj.model if isinstance(obj, QuerySet) else type(obj)
        
        if isinstance(self.serializer_classes, dict):
            SerializerClass = self.serializer_classes.get(ObjectClass)
            if SerializerClass:
                return SerializerClass
        elif isinstance(self.serializer_classes, (list, tuple)):
            for SerializerClass in self.serializer_classes:
                if compat.get_serializer_model(SerializerClass) is ObjectClass:
                    return SerializerClass
        else:
            raise TypeError('``serializer_classes`` value should be iterable or dict')

        return compat.create_serializer_class(ObjectClass)

    def get_serializer(self, obj):
        SerializerClass = self.get_serializer_class(obj)
        
        if SerializerClass is None:
            return None

        return compat.create_serializer(SerializerClass, obj)

    def serialize_included_context(self, context):
        serialized = {}
        for key, value in six.iteritems(context):
            if isinstance(value, (int, long, float, list, dict)):
                serialized[key] = value
            else:
                serializer = self.get_serializer(value)
                serialized[key] = compat.serialize(serializer) if serializer else value
            
        return serialized


class RendererProviderMixin(object):

    renderer_class = None
    angular_context_template_name = 'angularmagic/context-item.html'

    def get_renderer_class(self):
        if self.renderer_class:
            return self.renderer_class
        else:
            return appsettings.DEFAULT_RENDERER_CLASS

    def get_renderer(self, context):
        RendererClass = self.get_renderer_class()
        return compat.create_renderer(RendererClass, context)

    def render_included_context(self, context):
        renderer = self.get_renderer(context)
        return compat.render(renderer, context)

    def render_data_block(self, data_context):
        template_context = {
            'data': self.render_included_context(data_context),
            'DEBUG': settings.DEBUG,
        }
        return render_to_string(self.angular_context_template_name,
                                template_context)


class BaseAngularMagicMixin(object):

    def render_angular_app(self, angular_template, context):
        included_context = self.get_included_context(context)
        serialized_context = self.serialize_included_context(included_context)
        rendered_context = self.render_data_block(serialized_context)
        return rendered_context + angular_template

    def get_included_context(self, context):
        return {}


class AngularMagicMixin(BaseAngularMagicMixin,
                        SerializerProviderMixin,
                        RendererProviderMixin):
    pass    
    
