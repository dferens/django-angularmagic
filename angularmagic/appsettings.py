import datetime

from . import default
from .external import json


ANGULAR_TOKENS = {
    'VARIABLE_OPEN': '{{ ',
    'VARIABLE_CLOSE': ' }}'
}


DEFAULT_SERIALIZER_CLASS = default.Serializer
DEFAULT_RENDERER_CLASS = default.Renderer
