class Serializer(object):

    model = NotImplemented

    def __init__(self, obj):
        pass

    def serialize(self):
        raise NotImplementedError


class Renderer(object):

    format = NotImplemented

    def __init__(self, data):
        pass

    def render(self):
        raise NotImplementedError
