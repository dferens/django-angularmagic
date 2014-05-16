import json
from contextlib import contextmanager
import datetime

from django import template
from django.template.base import Node, Parser, TOKEN_VAR, TOKEN_TEXT

from .. import appsettings
from ..views import AngularMagicMixin

register = template.Library()


class AngularAppNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        view = context.get('view')
        angular_template = self.nodelist.render(context)
        if view and isinstance(view, AngularMagicMixin):
            return view.render_angular_app(angular_template, context)
        else:
            return angular_template


@contextmanager
def disable_variables_parsing(parser):
    def next_token():
        token = Parser.next_token(parser)
        if token.token_type == TOKEN_VAR:
            token.token_type = TOKEN_TEXT
            token.contents = (appsettings.ANGULAR_TOKENS['VARIABLE_OPEN'] +
                              token.contents +
                              appsettings.ANGULAR_TOKENS['VARIABLE_CLOSE'])
        return token

    try:
        parser.next_token = next_token
        yield
    finally:
        del parser.next_token


@register.tag('angularapp')
def angular_app(parser, token):
    with disable_variables_parsing(parser):
        nodelist = parser.parse(('endangularapp',))

    parser.delete_first_token()
    return AngularAppNode(nodelist)
