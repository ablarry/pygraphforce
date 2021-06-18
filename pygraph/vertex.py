class Vertex:
    """
    The Vertex class represents node in graphs
    :param id: Unique identifier of vertex
    :param attr: Properties of vertex
    """

    def __init__(self, id, attributes=None):
        self.id = id
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
