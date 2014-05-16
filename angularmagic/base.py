class Serializer(object):
    """
    Converts complex objects such as querysets or model instances to
    native Python datatypes that can be converted to xml/json/anything later.

    Is a light wrapper of ``rest_framework.serializers.Serializer``.

    :param model: class if serializer is class-specific.
    :type model: type
    """

    model = None

    def __init__(self, obj):
        """
        Initializes serializer instance.

        :param obj: object to serialize
        """
        pass

    def serialize(self):
        """
        Actually serializes previously passed object.

        :return: 
        """
        raise NotImplementedError


class Renderer(object):
    """
    Renders passed data to string.

    Is a light wrapper of ``rest_framework.renderers.Renderer``.

    :param format:  (like 'json' or 'xml')
    """

    format = 'unknown'

    def __init__(self, data):
        """
        Initializes renderer instance.

        :param data: data to render
        """
        pass

    def render(self):
        """
        Actually renders previously passed data.

        :return: rendered data as string
        """
        raise NotImplementedError
