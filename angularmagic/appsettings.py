import datetime

from .compat import json


ANGULAR_TOKENS = {
    'VARIABLE_OPEN': '{{ ',
    'VARIABLE_CLOSE': ' }}'
}


class DefaultRenderer(json.JSONEncoder):

    RENDER_RULES = {
        datetime.date: lambda d: d.isoformat(),
        datetime.time: lambda t: t.isoformat(),
        datetime.datetime: lambda d: d.isoformat(),
        datetime.timedelta: lambda td: td.isoformat(),
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(separators=(',', ':'))
        super(DefaultRenderer, self).__init__(*args, **kwargs)

    def default(self, obj):
        module, name = type(obj).__module__, type(obj).__name__
        render_rule = self.RENDER_RULES.get(type(obj)) or str
        return {'value': render_rule(obj),
                'py/object': '%s.%s' % (module, name)}


DEFAULT_RENDERER_CLASS = DefaultRenderer
