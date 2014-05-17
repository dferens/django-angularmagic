import json
from xml.dom.minidom import parseString
import mock

from django.test import TestCase

from angularmagic import appsettings, base, views

from ..generic.models import TestModel


class SerializerProviderMixinTestCase(TestCase):

    def test_get_serializer_from_dict(self):
        class TestModelSerializer(base.Serializer):
            def __init__(self, obj):
                self.serialize = lambda: obj

        class MyView(views.SerializerProviderMixin):
            serializer_classes = {TestModel: TestModelSerializer}

        obj, view = TestModel(), MyView()
        self.assertIsInstance(view.get_serializer(obj), TestModelSerializer)
        self.assertIsInstance(view.get_serializer('anything'),
                              appsettings.DEFAULT_SERIALIZER_CLASS)

    @mock.patch('angularmagic.views.external')
    def test_get_serializer_from_list(self, mock_external):
        class GenericSerializer(base.Serializer): pass

        class ExternalSerializer(object):
            model = None

        class NativeModelSerializer(base.Serializer):
            model = TestModel

            def serialize(self): pass

        class ExternalModelSerializer(object):
            model = TestModel

        class MyView(views.SerializerProviderMixin):
            serializer_classes = None

        obj, view = TestModel(), MyView()
        
        MyView.serializer_classes = [GenericSerializer, NativeModelSerializer]
        self.assertIsInstance(view.get_serializer(obj), NativeModelSerializer)

        MyView.serializer_classes = [ExternalSerializer, ExternalModelSerializer]
        mock_external.create_serializer_adapter = lambda Class, o: Class()  
        self.assertIsInstance(view.get_serializer(obj), ExternalModelSerializer)

    def test_get_serializer_from_empty_list(self):
        class MyView(views.SerializerProviderMixin):
            serializer_classes = []

        obj, view = TestModel(), MyView()
        self.assertIsInstance(view.get_serializer(obj),
                              appsettings.DEFAULT_SERIALIZER_CLASS)

    def test_get_serializer_from_other(self):
        class MyView(views.SerializerProviderMixin):
            serializer_classes = 'string'

        self.assertRaises(TypeError, MyView().get_serializer, 'anything')

    def test_get_serializer_by_queryset(self):
        obj = TestModel.objects.none()  # Empty queryset

        class Serializer(base.Serializer): pass

        class MyView(views.SerializerProviderMixin):
            serializer_classes = {TestModel: Serializer}

        self.assertIsInstance(MyView().get_serializer(obj), Serializer)

    @mock.patch('angularmagic.views.external')
    def test_get_serializer_creates_adapter(self, mock_external):
        class ExternalSerializer(object): pass

        class MyView(views.SerializerProviderMixin):
            serializer_classes = {TestModel: ExternalSerializer}

        obj = TestModel()
        MyView().get_serializer(obj)
        mock_get_adapter = mock_external.create_serializer_adapter
        mock_get_adapter.assert_called_once_with(ExternalSerializer, obj)

    def test_serialize_included_context(self):
        class Serializer(base.Serializer):
            def serialize(self): return 'serialized'

        class MyView(views.SerializerProviderMixin):
            serializer_classes = {TestModel: Serializer}

        serialize = MyView().serialize_included_context
        # Empty context
        self.assertEqual(serialize({}), {})
        # Primitives
        self.assertEqual(serialize({'one': 1}), {'one': 1})
        # Complex objects
        self.assertEqual(serialize({'obj': TestModel()}), {'obj': 'serialized'})


class RendererProviderMixinTestCase(TestCase):

    def test_render_data_block(self):
        class Renderer(base.Renderer):
            def __init__(self, data):
                self.render = lambda: json.dumps(data)

        class MyView(views.RendererProviderMixin):
            renderer_class = Renderer

        view = MyView()
        data = {'number': 1, 'obj': {'id': 1, 'text': 'test'}}
        block_dom = parseString(view.render_data_block(data)).childNodes[0]
        self.assertEqual(block_dom.nodeName, 'django-context-item')        
        self.assertEqual(block_dom.attributes['bytes'].value, '47')
        self.assertEqual(data, json.loads(block_dom.childNodes[0].nodeValue))


class BaseAngularMagixMixinTestCase(TestCase):
    
    def test_render_angular_app(self):
        class MyView(views.AngularMagicMixin):
            data = {'number': 1, 'obj': {'id': 1, 'text': 'test'}}
            def get_included_context(self, context):
                return self.data

        view = MyView()
        html = view.render_angular_app('<div ng-app="app">{{view}}</div>', None)
        dom = parseString('<html>%s</html>' % html).childNodes[0]
        data_node, template_node = dom.childNodes[0], dom.childNodes[-1]
        self.assertEqual(template_node.childNodes[0].nodeValue, '{{view}}')
        self.assertEqual(json.loads(data_node.childNodes[0].nodeValue), view.data)

    def test_get_included_context_warns_about_super(self):
        class MyView(views.AngularMagicMixin):
            pass

        with self.assertRaises(NotImplementedError):
            MyView().get_included_context({})
