import math
import random
from random import randint
from random import random

from pygraph import edge
from pygraph import graph
from pygraph import vertex

# Coordinates 
COORDINATE_X = "x"
COORDINATE_Y = "y"


def mesh(m, n, directed=False):
    """
    Creates a graph of m*n nodes
    :param m: number of columns (>1)
    :param n: number of rows (>1)
    :param directed: enable graph directed
    :return: Graph created
    """
    # Parameter's validation
    if m <= 1 or n <= 1:
        raise ValueError("m,n parameters must to be > 1")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    for i in range(m * n):
        v = vertex.Vertex(i)
        g.add_vertex(v)
    index = 0
    for i in range(m):
        for j in range(n):
            if i != (m - 1):
                g.add_edge(edge.Edge(index, (index + n)), directed)
            if j != (n - 1):
                g.add_edge(edge.Edge(index, (index + 1)), directed)
            index = index + 1
    return g


def erdos_rengy(n, m, directed=False, auto=False):
    """
    Creates a graph of n nodes with model Erdos-Renyi
    :param n: number of nodes ( > 0)
    :param m: number of edges ( >= n-1)
    :param directed: enable graph directed
    :param auto: allow auto-cycle (loops)
    :return: Graph created
    """
    # Parameter's validation
    if n <= 0:
        raise ValueError("n parameter must to be > 0 ")
    if m < n - 1:
        raise ValueError("m parameter must to be >= n-1 ")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    for i in range(n):
        g.add_vertex(vertex.Vertex(i))
    edges = {}
    while len(g.edges) != m:
        # Create random m different edges
        source = randint(0, m - 1)
        target = randint(0, m - 1)
        e = (source, target)
        if e not in edges:
            edges[e] = e
            g.add_edge(edge.Edge(source, target), directed, auto)
    return g


def gilbert(n, p, directed=False, auto=False):
    """
    Creates a graph of n nodes with model Gilbert 
    :param n: number of nodes ( > 0)
    :param p: probability to create an edge (0,1)
    :param directed: enable graph directed
    :param auto: allow auto-cycle (loops)
    :return: Graph created
    """
    # Parameter's validation
    if n <= 0:
        raise ValueError("n parameter must to be > 0 ")
    if p <= 0 or p >= 1:
        raise ValueError("p parameter must to be in range (0,1)")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    for i in range(n):
        g.add_vertex(vertex.Vertex(i))
    for i in range(n):
        for j in range(n):
            # Create edge with probability => random number (0,1) 
            if random() <= p:
                g.add_edge(edge.Edge(i, j), directed, auto)

    return g


def geo_simple(n, r, directed=False, auto=False):
    """
    Create a random graph with simple method geographic
    :param n: number of vertices ( > 0)
    :param r: max distance to generate edge between nodes (0,1)
    :param directed: enable graph directed
    :param auto: allow auto-cycle (loops)
    :return: graph created
    """
    # Parameter's validation
    if n <= 0:
        raise ValueError("n parameter must to be > 0 ")
    if r <= 0 or r >= 1:
        raise ValueError("r parameter must to be in range (0,1)")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    # Create n nodes with uniform coordinates 
    for i in range(n):
        g.add_vertex(
            vertex.Vertex(i, {COORDINATE_X: random(), COORDINATE_Y: random()}))

    # Create edge between two vertex if there is a distance <= r
    for i in range(n):
        for j in range(n):
            # Calculate distance between two points
            p1 = (g.get_vertex(i).attributes[COORDINATE_X],
                  g.get_vertex(i).attributes[COORDINATE_Y])
            p2 = (g.get_vertex(j).attributes[COORDINATE_X],
                  g.get_vertex(j).attributes[COORDINATE_Y])
            d = calculate_distance(p1, p2)
            if d <= r:
                g.add_edge(edge.Edge(i, j), directed, auto)
    return g


def barabasi(n, d, directed=False, auto=False):
    """
    Create Barabasi-Albert (BA) graph
    :param n: number of nodes ( > 0)
    :param d: max number of edges of vertex ( > 1)
    :param directed: enable graph directed
    :param auto: allow auto-cycle (loops)
    return: graph created
    """
    # Parameter's validation
    if n <= 0:
        raise ValueError("n parameter must to be > 0 ")
    if d <= 1:
        raise ValueError("d parameter must to be > 1")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    # The first d vertices are created with edges to relate each one with the others
    for i in range(d):
        g.add_vertex(vertex.Vertex(i))
    for i in range(d):
        for j in range(d):
            if len(g.get_edges_by_vertex(i)) < d and len(
                    g.get_edges_by_vertex(j)) < d:
                g.add_edge(edge.Edge(i, j), directed, auto)

    for i in range(d, n):
        g.add_vertex(vertex.Vertex(i))
        for j in range(i):
            # The probability p that the new node i is connected to node j
            # is the grade of vertex j divided by the number of edges of graph
            p = len(g.get_edges_by_vertex(j)) / len(g.get_edges())
            if len(g.get_edges_by_vertex(i)) < d and len(
                    g.get_edges_by_vertex(j)) < d and p >= random():
                g.add_edge(edge.Edge(i, j), directed, auto)
    return g


def dorogovtsev_mendes(n, directed=False):
    """
    Create a Dorogovtsev-Mendes graph
    :param n: number of nodes
    :param directed: enable graph directed
    :return: graph created
    """
    # Parameter's validation
    if n < 3:
        raise ValueError("n parameter must to be >= 3 ")

    g = graph.Graph()
    # Add attribute DIRECTED in graph
    g.attr[graph.DIRECTED] = directed

    # Create 3 vertex and 3 edges to form triangle
    for i in range(3):
        g.add_vertex(vertex.Vertex(i))
    for i in range(3):
        j = i + 1 if i < 2 else 0
        g.add_edge(edge.Edge(i, j), directed)

    # To add next vertices one by one, choosing randomly one edge of the grap
    # and create edges between new vertice and origin and source of edge selected 
    for i in range(3, n):
        g.add_vertex(vertex.Vertex(i))
        # Select random edge of the graph
        id_edge = randint(0, len(g.get_edges()) - 1)
        edge_selected = g.get_edges()[id_edge]
        (source, target) = edge_selected
        # Create edges between new vertice and origin and source of edge selected 
        g.add_edge(edge.Edge(i, source), directed)
        g.add_edge(edge.Edge(i, target), directed)

    return g


def calculate_distance(p1, p2):
    """
    Calculate distance between two points
    param p1: tuple (x,y) point1
    param p2: tuple (x,y) point2
    return: distance between two points
    """
    x1, y1 = p1
    x2, y2 = p2
    d = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    return d
