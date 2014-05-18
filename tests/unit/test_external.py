import mock
from decimal import Decimal
import contextlib

from django.db import models
from django.test import TestCase

from rest_framework.serializers import Serializer, ModelSerializer
from tastypie.resources import Resource, ModelResource

import angularmagic.external

from ..generic.models import TestModel


@contextlib.contextmanager
def disable(*module_names):
    """
    Disables external modules.

    :param module_names: 'tastypie', etc.
    :type module_names: str
    """
    assert module_names
    kwargs = dict((k, mock.DEFAULT) for k in module_names)
    with mock.patch.multiple(angularmagic.external, **kwargs) as mocks:
        for mocked_module in mocks.values():
            mocked_module.__nonzero__ = mock.Mock(return_value=False)

        yield


class ExternalTestCase(TestCase):

    class BadSerializer(object): pass

    def get_adapter(self, SerializerClass, obj=None):
        args = (SerializerClass, obj or mock.Mock())
        return angularmagic.external.create_serializer_adapter(*args)


class CreateSerializerAdapterTestCase(ExternalTestCase):

    @mock.patch('angularmagic.external.RestFrameworkSerializerAdapter')
    def test_rest_framework(self, SerializerAdapterClass):
        SerializerAdapterClass.return_value = 'rf adapter'

        class CustomSerializer(Serializer):
            pass

        with disable('rest_framework'):
            self.assertRaises(TypeError, self.get_adapter, CustomSerializer)

        self.assertEqual(self.get_adapter(CustomSerializer), 'rf adapter')
        self.assertRaises(TypeError, self.get_adapter, self.BadSerializer)

    @mock.patch('angularmagic.external.TastypieSerializerAdapter')
    def test_tastypie(self, SerializerAdapterClass):
        SerializerAdapterClass.return_value = 'tp adapter'

        class CustomResource(Resource):
            pass

        with disable('tastypie'):
            self.assertRaises(TypeError, self.get_adapter, CustomResource)

        self.assertEqual(self.get_adapter(CustomResource), 'tp adapter')
        self.assertRaises(TypeError, self.get_adapter, self.BadSerializer)


class SerializerAdaptersTestCase(ExternalTestCase):

    class TestSerializer(Serializer): pass
    
    class TestModelSerializer(ModelSerializer):
        class Meta:
            model = TestModel

    class TestResource(Resource):
        class Meta:
            include_resource_uri = False

    class TestModelResource(ModelResource):
        class Meta:
            include_resource_uri = False
            queryset = TestModel.objects.all()

    SimpleSerializers = (TestSerializer, TestResource)
    ModelSerializers = (TestModelSerializer, TestModelResource)

    def test_init(self):
        def run_simple(SerializerClass):
            adapter = self.get_adapter(SerializerClass)
            self.assertEqual(adapter.model, None)
            self.assertIsInstance(adapter.obj, mock.Mock)

        def run_model(SerializerClass):
            adapter = self.get_adapter(SerializerClass)
            self.assertEqual(adapter.model, TestModel)
            self.assertIsInstance(adapter.obj, mock.Mock)

        map(run_simple, self.SimpleSerializers)
        map(run_model, self.ModelSerializers)

    def test_serialize_single(self):
        obj = TestModel()

        def run_simple(SerializerClass):
            adapter = self.get_adapter(SerializerClass, obj)
            self.assertEqual(adapter.serialize(), {})

        def run_model(SerializerClass):
            adapter = self.get_adapter(SerializerClass, obj)
            self.assertEqual(adapter.serialize(), {
                'id': 1,
                'number': obj.number,
                'text': obj.text,
                'salary': obj.salary    
            })
        
        map(run_simple, self.SimpleSerializers)
        map(run_model, self.ModelSerializers)

    def test_serialize_collection(self):
        obj_list = [TestModel(id=1, number=1, text='test', salary=Decimal('0.1')),
                    TestModel(id=2, number=2, text='test_2', salary=Decimal('0.2'))]
        expected = [{'id': 1,
                     'number': 1,
                     'text': 'test',
                     'salary': obj_list[0].salary},
                    {'id': 2,
                     'number': 2,
                     'text': 'test_2',
                     'salary': obj_list[1].salary}]

        def run_simple(SerializerClass):
            adapter = self.get_adapter(SerializerClass, obj_list)
            self.assertEqual(adapter.serialize(), [{}, {}])

        def run_model(SerializerClass):
            adapter = self.get_adapter(SerializerClass, obj_list)
            self.assertEqual(adapter.serialize(), expected)

        map(run_simple, self.SimpleSerializers)
        map(run_model, self.ModelSerializers)
