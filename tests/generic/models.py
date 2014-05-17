from decimal import Decimal

from django.db import models


class TestModel(models.Model):
    class Meta:
        managed = False

    number = models.IntegerField()
    text = models.TextField()
    salary = models.DecimalField(decimal_places=2, max_digits=10)

    def __init__(self, **kwargs):
        kwargs.setdefault('id', 1)
        kwargs.setdefault('number', 1)
        kwargs.setdefault('text', 'test')
        kwargs.setdefault('salary', Decimal('1.2'))
        super(TestModel, self).__init__(**kwargs)
