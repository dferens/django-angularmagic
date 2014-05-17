from django.conf import settings
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils import six

from . import appsettings, base, external


class SerializerProviderMixin(object):

    serializer_classes = []
    primitive_types = (int, long, float, list, dict) + six.string_types

    def get_serializer(self, obj):
        """
        :return: ``angularmagic.base.Serializer`` instance
        """
        SerializerClass = None
        if isinstance(obj, QuerySet):
            ObjectClass = obj.model
        else:
            ObjectClass = type(obj)

        if isinstance(self.serializer_classes, dict):
            SerializerClass = self.serializer_classes.get(ObjectClass, SerializerClass)
        elif isinstance(self.serializer_classes, (list, tuple)):
            for Class in self.serializer_classes:
                if issubclass(Class, base.Serializer):
                    if Class.model is ObjectClass:
                        SerializerClass = Class
                        break
                else:
                    adapter = external.create_serializer_adapter(Class, obj)
                    if adapter.model is ObjectClass:
                        return adapter
        else:
            raise TypeError('``serializer_classes`` value should be iterable or dict')

        SerializerClass = SerializerClass or appsettings.DEFAULT_SERIALIZER_CLASS
        if issubclass(SerializerClass, base.Serializer):
            return SerializerClass(obj)
        else:
            return external.create_serializer_adapter(SerializerClass, obj)
        
    def serialize_included_context(self, context):
        serialized = {}
        for key, value in six.iteritems(context):
            if isinstance(value, self.primitive_types):
                serialized[key] = value
            else:
                serializer = self.get_serializer(value)
                serialized[key] = serializer.serialize() if serializer else value

        return serialized


class RendererProviderMixin(object):

    renderer_class = None
    angular_context_template_name = 'angularmagic/context-item.html'

    def get_renderer(self, context):
        RendererClass = self.renderer_class or appsettings.DEFAULT_RENDERER_CLASS
        return RendererClass(context)

    def render_included_context(self, context):
        renderer = self.get_renderer(context)
        return renderer.render()

    def render_data_block(self, data_context):
        rendered_context = self.render_included_context(data_context)
        template_context = {
            'data': rendered_context,
            'bytes': len(rendered_context),
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
    
