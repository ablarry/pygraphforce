import collections
import sys

from graphviz import Digraph
from graphviz import Graph as Graphviz

from pygraph import edge
from pygraph import vertex

# Attribute to indicate if is a directed graph
DIRECTED = "DIRECTED"

# Render images graphviz
RENDER = False

# Attribute to inidcate if a vertes has been discovered
DISCOVERED = "DISCOVERED"


class Graph:
    def __init__(self, vertices=None, edges=None, attr={}):
        """__init__ initializes Graph object. Graph stores vertices and edges
           param vertices: Dictionary with vertices
           param edges:    Dictionary with edges
           param attr:     Properties of graph
        """
        if vertices is None:
            vertices = {}
        self.vertices = vertices

        if edges is None:
            edges = {}
        self.edges = edges

        self.attr = attr

    def add_vertex(self, vertex):
        """ add_vertex add vertex to graph's vertices
            if there is not other vertex with same id
            param vertex: vertex to add in graph
        """
        if vertex.id not in self.vertices.keys():
            self.vertices[vertex.id] = vertex

    def get_vertices(self):
        return self.vertices

    def get_vertex(self, id):
        if id in self.vertices.keys():
            return self.vertices[id]
        else:
            return None

    def add_edge(self, edge, directed=False, auto=False):
        """ Add edge to source edges
            if there is no other edge with same source and target
            :param edge: edge to insert
            :param directed: enable graph directed
            :param auto: allow auto-cycle (loops)
        """
        (v1, v2) = edge.get_id()
        if v1 in self.vertices.keys() and v2 in self.vertices.keys():
            if directed:
                if auto:
                    self.edges[edge.get_id()] = edge
                else:
                    if v1 != v2:
                        self.edges[edge.get_id()] = edge
            else:
                if self.edges.get((v2, v1)) is None:
                    if auto:
                        self.edges[edge.get_id()] = edge
                    else:
                        if v1 != v2:
                            self.edges[edge.get_id()] = edge

    def get_edges(self):
        """ edges create edges of the graph
        """
        edges = []
        for (key, target) in self.edges.keys():
            edges.append((key, target))
        return edges

    def get_edge(self, id, directed=False):
        """
        Get edge by specific id
        param id: Tupla identifier of edge
        param directed: Filter to find edge directed
        """
        (u, v) = id
        for (source, target) in self.edges.keys():
            if directed:
                if (source, target) == (u, v):
                    return self.edges[(source, target)]
            else:
                if (source, target) == (u, v) or (source, target) == (v, u):
                    return self.edges[(source, target)]
        return None

    def get_adjacent_vertices_by_vertex(self, id, type=None):
        """
        Get adjacent vertex of specific vertex
        param id: Vertex identifier in the graph
        param type: Filter
            None - All adjacent vertices
            +    - Output adjacent vertices
            -    - Input adjacent vertices
        """
        vertex = []
        for (source, target) in self.edges.keys():
            if type is None:
                if source == id:
                    vertex.append(target)
                elif target == id:
                    vertex.append(source)
            elif type == '+':
                if source == id:
                    vertex.append(target)
            elif type == '-':
                if target == id:
                    vertex.append(source)

        return vertex

    def get_edges_by_vertex(self, id, type=0):
        """
        Find the edges that are incident in vertex with id paramater
        param id: Vertex identifier in the graph
        param type: Filter output edges
            1 - Output edges
            2 - Input edges
            other - All edges
        return: list of edges
        """
        edges = []
        for (source, target) in self.edges.keys():
            if type == 1:
                if source == id:
                    edges.append((source, target))
            elif type == 2:
                if target == id:
                    edges.append((source, target))
            else:
                if source == id or target == id:
                    edges.append((source, target))
        return edges

    def clone(self):
        """
        Clone graph
        return: Clone graph
        """
        g = Graph(attr=self.attr.copy(), vertices=self.vertices.copy(),
                  edges=self.edges.copy())
        return g


    def create_graphviz(self, file_name, attr_label_vertex=None, source=None,
                        attr_label_edge=None):
        dot = Graphviz()

        # Review attribute directed of graph
        if DIRECTED in self.attr:
            if self.attr[DIRECTED]:
                dot = Digraph()
            else:
                dot = Graphviz()
        if attr_label_vertex is None:
            # Map graph to graphviz structure
            for n in list(self.vertices.keys()):
                dot.node(str(n), str(n))
        else:
            # Map graph to graphviz structure and add vertex attribute
            for n in list(self.vertices.keys()):
                label = "Node: " + str(n)
                source_label = "Node source: " + str(
                    source) if source is not None else ""
                label = label + "\n" + source_label
                label = label + "\n" + attr_label_vertex + " (" + str(
                    self.vertices[n].attributes[attr_label_vertex]) + ")"
                dot.node(str(n), label)

        if attr_label_edge is None:
            for e in self.get_edges():
                (s, t) = e
                dot.edge(str(s), str(t))
        else:
            for e in self.get_edges():
                (s, t) = e
                label_edge = self.edges[(s, t)].attr["WEIGHT"]
                dot.edge(str(s), str(t), label=str(label_edge))

        file = open("./images/gv/" + file_name + ".gv", "w")
        file.write(dot.source)
        file.close()
        return dot

    def bfs(self, s):
        """
        bfs Breadth-first search (BFS) is an algorithm
        for traversing or searching graph data structures.
        It starts at the s node
        and explores all of the neighbor nodes at the present
        depth prior to moving on to the nodes at the next depth level.
        :param s: root node for traversing
        :return g graph generated according BFS
        """
        g = Graph(attr={DIRECTED: True})
        root = self.get_vertex(s)
        root.attributes[DISCOVERED] = True
        q = collections.deque()
        adjacent_type = '+' if DIRECTED in self.attr and self.attr[
            DIRECTED] else None
        # Insert root node in graph and queue
        g.add_vertex(root)
        q.append(s)

        while (len(q) > 0):
            v = q.popleft()
            for e in self.get_adjacent_vertices_by_vertex(v, adjacent_type):
                w = self.get_vertex(e)
                if DISCOVERED not in w.attributes or w.attributes[
                    DISCOVERED] is False:
                    w.attributes[DISCOVERED] = True
                    q.append(w.id)
                    g.add_vertex(w)
                    g.add_edge(edge.Edge(v, e), True)
        return g

    def dfs(self, s):
        """
        dfs Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. 
        The algorithm starts at the root node and explores as far as possible along each branch before backtracking.
        :param s: root node for traversing
        :return g graph generated according DFS 
        """
        g = Graph(attr={DIRECTED: True})
        adjacent_type = '+' if DIRECTED in self.attr and self.attr[
            DIRECTED] else None
        # Insert s root node in stack 
        stack = collections.deque()
        # Initial node does not have origin, it is represented by # 
        stack.append(('#', s))

        while (len(stack) > 0):
            (source, target) = stack.pop()
            w = self.get_vertex(target)
            if DISCOVERED not in w.attributes or w.attributes[
                DISCOVERED] is False:
                w.attributes[DISCOVERED] = True
                g.add_vertex(w)
                if (source != '#'):
                    g.add_edge(edge.Edge(source, w.id), True)
                for e in self.get_adjacent_vertices_by_vertex(w.id,
                                                              adjacent_type):
                    stack.append((w.id, e))
        return g

    def dfs_r(self, s):
        """
        dfs Depth-first search (DFS) recursive is an algorithm for traversing or searching tree
        or graph data structures. 
        The algorithm starts at the root node and explores as far as possible along each branch
        before backtracking.
        :param s: root node for traversing
        :return g graph generated according DFS 
        """
        g = Graph(attr={DIRECTED: True})
        return self.dfs_rec(g, ('#', s))

    def dfs_rec(self, g, s):
        adjacent_type = '+' if DIRECTED in self.attr and self.attr[
            DIRECTED] else None
        (source, target) = s
        w = self.get_vertex(target)
        if DISCOVERED not in w.attributes or w.attributes[DISCOVERED] is False:
            w.attributes[DISCOVERED] = True
            g.add_vertex(w)
            if (source != '#'):
                g.add_edge(edge.Edge(source, w.id), True)
            for e in self.get_adjacent_vertices_by_vertex(w.id, adjacent_type):
                self.dfs_rec(g, (w.id, e))
        return g

    def dijkstra(self, s, t):
        """
        dijkstra is an algorithm for finding the shortest paths between nodes in a graph.
        :param s: node source
        :param t: node target
        :return g graph generated with the shortest path from source to target 
        """
        l = []
        dist = {}
        prev = {}
        discovered = {}
        for v in self.get_vertices():
            dist[v] = float('inf')
            prev[v] = None
            discovered[v] = False
        dist[s] = 0
        l.append((s, dist[s]))
        while len(l) != 0:
            u = min(l, key=lambda x: x[1])
            l.remove(u)
            u = u[0]
            discovered[u] = True
            if u == t:
                break
            for v in self.get_adjacent_vertices_by_vertex(u):
                if not discovered[v]:
                    alt = dist[u] + self.get_edge((u, v)).attr["WEIGHT"]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        l.append((v, dist[v]))
        # Create a graph according to visited nodes store in prev array
        u = t
        g = Graph(attr={DIRECTED: True})
        while u is not None:
            g.add_vertex(vertex.Vertex(u, {"WEIGHT": dist[u]}))
            if prev[u] is not None:
                g.add_vertex(vertex.Vertex(prev[u], {"WEIGHT": dist[prev[u]]}))
                g.add_edge(edge.Edge(prev[u], u))
                u = prev[u]
            else:
                break
        return g

    def dijkstra_tree(self, s):
        """
        dijkstra_tree is an algorithm for finding tree of cost for each node according Dijkstra's algorithm.
        :param s: node source
        :param t: node target
        :return g graph generated with the shortest path from source to target 
        """
        l = []
        dist = {}
        prev = {}
        discovered = {}
        g = Graph(attr={DIRECTED: True})
        g.add_vertex(vertex.Vertex(s, {"WEIGHT": 0}))
        for v in self.get_vertices():
            dist[v] = float('inf')
            prev[v] = None
            discovered[v] = False
        dist[s] = 0
        l.append((s, dist[s]))
        while len(l) != 0:
            u = min(l, key=lambda x: x[1])
            l.remove(u)
            u = u[0]
            discovered[u] = True
            for v in self.get_adjacent_vertices_by_vertex(u):
                if not discovered[v]:
                    alt = dist[u] + self.get_edge((u, v)).attr["WEIGHT"]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        l.append((v, dist[v]))
                        g.add_vertex(vertex.Vertex(v, {"WEIGHT": dist[v]}))
                        g.add_edge(edge.Edge(u, v, {"WEIGHT": dist[v]}))

        return g

    def find(self, parent, i):
        """
        find is a utility function to find set of an element i
        :param parent: parent node source
        :param i: node source
        """
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def KruskalD(self):
        """
        KruskalD is a function based on Krustal's algorithm to find a minimum spanning forest of an undirected edge-weighted graph. 
        :return g graph representing minimum spannng forest 
        """
        g = Graph(attr={DIRECTED: False})
        # Create set for each v of V[G]
        parent = []
        rank = []
        for v in self.get_vertices():
            parent.append(v)
            rank.append(0)

        # Sort edges by weight
        q = sorted(self.edges.items(), key=lambda e: e[1].attr["WEIGHT"])
        for e in q:
            (u, v) = e[0]
            v1 = self.find(parent, u)
            v2 = self.find(parent, v)
            if v1 != v2:
                g.add_vertex(vertex.Vertex(u))
                g.add_vertex(vertex.Vertex(v))
                g.add_edge(edge.Edge(u, v, {"WEIGHT": e[1].attr["WEIGHT"]}))
                if rank[v1] < rank[v2]:
                    parent[v1] = v2
                    rank[v2] += 1
                else:
                    parent[v2] = v1
                    rank[v1] += 1
        return g

    def Kruskal(self):
        """
        Kruskal is a function based on Inverse Krustal's algorithm to find a minimum spanning forest of an undirected edge-weighted graph. 
        :return g graph representing minimum spannng forest 
        """
        g = self.clone()
        # Sort edges by weight descendent
        q = sorted(self.edges.items(), key=lambda e: e[1].attr["WEIGHT"],
                   reverse=True)
        for e in q:
            # remove e  
            g.edges.pop(e[0])
            # clear weight
            for k in self.vertices:
                g.vertices[k].attributes["DISCOVERED"] = False
            # valid if there is connected graph 
            if len(g.vertices) != len(g.bfs(0).vertices):
                g.add_edge(e[1])
        return g

    def Prim(self):
        """
        Prim is a function based on  Prim's algorithm to find a minimum spanning forest of an undirected edge-weighted graph. 
        :return g graph representing minimum spannng forest 
        """
        g = Graph(attr={DIRECTED: False})
        distance = [sys.maxsize] * len(self.vertices)
        parent = [None] * len(self.vertices)
        set = [False] * len(self.vertices)

        distance[0] = 0
        parent[0] = -1

        for i in self.vertices:
            # Search vertex with minimum distance
            min_index = 0
            min = sys.maxsize
            for v in self.vertices:
                if distance[v] < min and set[v] is False:
                    min = distance[v]
                    min_index = v
            u = min_index

            # Add u vertex in set to not use it in other iteration 
            set[u] = True
            g.add_vertex(vertex.Vertex(u))

            # Iterate all adjacent vertices of u vertex and update distance 
            for v in self.get_adjacent_vertices_by_vertex(u):
                if set[v] is False and distance[v] > \
                        self.get_edge((u, v)).attr["WEIGHT"]:
                    distance[v] = self.get_edge((u, v)).attr["WEIGHT"]
                    parent[v] = u

        for i in self.vertices:
            if i == 0:
                continue
            if parent[i] is not None:
                g.add_edge(edge.Edge(parent[i], i, {"WEIGHT": self.get_edge((parent[i], i)).attr["WEIGHT"]}))

        return g
