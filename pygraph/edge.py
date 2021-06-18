class Edge:
    """
    Initializes edge with source and target
    :param source: origin point
    :param target: end pint
    """

    def __init__(self, source, target, attr=None):
        self.source = source
        self.targer = target
        self.edge = (source, target)
        if attr is None:
            self.attr = {}
        else:
            self.attr = attr

    def get_id(self):
        """
        Returns tupla (source, target) to identify Edge
        """
        return self.edge
