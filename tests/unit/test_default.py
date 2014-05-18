import json
from decimal import Decimal

from django.db import models
from django.test import TestCase

from angularmagic.default import Serializer, Renderer

from ..generic.models import TestModel


class RendererTestCase(TestCase):

    def setUp(self):
        self.renderer = Renderer(None)

    def render(self, data):
        self.renderer.data = data
        return self.renderer.render()

    def test_render_simple(self):
        self.assertIn(self.render(dict(one=1, two='two')),
                      ['{"one":1,"two":"two"}', '{"two":"two","one":1}'])

    def test_render_default(self):
        import datetime

        class CustomClass(object):
            def __str__(self):
                return '<CustomClass instance>'

        today, now = datetime.date.today(), datetime.datetime.now()
        CustomClass.__module__ = 'testmodule'
        data = dict(date_obj=today, datetime_obj=now,
                    custom_obj=CustomClass())
        json_data = json.loads(self.render(data))
        self.assertEqual(json_data, {
            'date_obj': {
                'py/object': 'datetime.date',
                'value': today.isoformat()
            },
            'datetime_obj': {
                'py/object': 'datetime.datetime',
                'value': now.isoformat()
            },
            'custom_obj': {
                'py/object': 'testmodule.CustomClass',
                'value': '<CustomClass instance>'
            }
        })


class SerializerTestCase(TestCase):

    def testmodel_instance_gen(self):
        number, base_text, salary  = 0, 'test', Decimal('0.0')

        while True:
            number += 1
            text = '%s_%s' % (base_text, number)
            salary += Decimal('0.1')
            obj = TestModel(id=number, number=number, text=text, salary=salary)
            yield obj

    def setUp(self):
        self.serializer = Serializer(None)

    def serialize(self, obj):
        self.serializer.obj = obj
        return self.serializer.serialize()

    def test_serialize_nonmodel_objects(self):
        class NonModelClass(object):
            class_attribute = 1

            def __init__(self):
                self.instance_attribute = 2

        obj = NonModelClass()
        obj_list = [NonModelClass() for x in range(5)]
        self.assertEqual(self.serialize(obj), obj)
        self.assertEqual(self.serialize(obj_list), obj_list)

    def test_serialize_model_objects(self):
        obj = next(self.testmodel_instance_gen())
        self.assertEqual(self.serialize(obj), dict(
            id=1, number=1, text='test_1', salary=Decimal('0.1')
        ))

        instance_gen = self.testmodel_instance_gen()
        obj_list = [next(instance_gen) for i in range(2)]
        self.assertEqual(self.serialize(obj_list), [
            {'id': 1,
             'number': 1,
             'text': 'test_1',
             'salary': Decimal('0.1')},
            {'id': 2,
             'number': 2,
             'text': 'test_2',
             'salary': Decimal('0.2')}
        ])

    def test_serialize_empty_collection(self):
        self.assertEqual(self.serialize([]), [])
