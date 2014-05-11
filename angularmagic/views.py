from django.utils import six

from . import appsettings, compat


class SerializerProviderMixin(object):

    serializer_classes = []

    def get_serializer_class(self, obj):
        if isinstance(self.serializer_classes, dict):
            return self.serializer_classes.get(type(obj))
        elif isinstance(self.serializer_classes, (list, tuple)):
            for SerializerClass in self.serializer_classes:
                is_serializer, ModelClass = compat.is_serializer(SerializerClass)
                if is_serializer and type(obj) is ModelClass:
                    return SerializerClass
        else:
            raise TypeError('``serializer_classes`` value should be iterable or dict')

    def serialize_included_context(self, context):
        serialized = {}
        for key, value in six.iteritems(context):
            SerializerClass = self.get_serializer_class(value)

            if SerializerClass is None:
                serialized[key] = value
            else:
                serialized[key] = compat.serialize(SerializerClass(), value)
            
        return serialized


class SerializerBuilderMixin(object):

    def get_serializer_class(self, obj):
        SerializerClass = super(SerializerBuilderMixin, self).get_serializer_class(obj)
        return SerializerClass or compat.serializer_factory(obj)


class RendererProviderMixin(object):

    renderer_class = None

    def get_renderer_class(self):
        if self.renderer_class:
            return self.renderer_class
        else:
            return appsettings.DEFAULT_RENDERER_CLASS

    def get_renderer(self):
        return self.get_renderer_class()()

    def render_included_context(self, context):
        renderer = self.get_renderer()
        return compat.render(renderer, context)

    def render_data_block(self, context):
        rendered_context = self.render_included_context(context)
        tmpl = '<django-context-item style="display:none">%s</django-context-item>'
        return tmpl % (rendered_context,)


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
                        SerializerBuilderMixin,
                        RendererProviderMixin):
    pass    
    
