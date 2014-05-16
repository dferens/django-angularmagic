from django.test import TestCase
from django.template import Context, Template
from django.views.generic import TemplateView


class AngularappTagTestCase(TestCase):

    def test_without_view(self):
        template = Template('{% load angularmagic %}'
                            '{{ var1 }}'
                            '{% angularapp %}{{ var2 }}{% endangularapp %}'
                            '{{ var3 }}')
        vars = {'var1': 1, 'var2': 2, 'var3': 3}
        expected = '1{{ var2 }}3'
        self.assertEqual(template.render(Context(vars)), expected)

    def test_with_view(self):
        from angularmagic.views import AngularMagicMixin

        ViewClass = type('View', (AngularMagicMixin, TemplateView), dict(
            get_included_context=lambda self, c: {'one': 1},
            render_angular_app=lambda self, tmpl, c: '<data>%s' % tmpl,
        ))
        template = Template('{% load angularmagic %}'
                            '{{ var1 }}'
                            '{% angularapp %}{{ var2 }}{% endangularapp %}'
                            '{{ var3 }}')
        context = Context(dict(var1=1, var2=2, var3=3, view=ViewClass()))
        expected = '1<data>{{ var2 }}3'
        self.assertEqual(template.render(context), expected)
