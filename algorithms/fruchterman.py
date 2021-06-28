import math
import time
import random

from screen.screen import Screen
from screen.vector import Vector


class Fruchterman:
    def __init__(self, graph, ):
        self.graph = graph
        self.positions = {}
        self.w = 1400
        self.l = 800
        self.t = 1
        self.screen = Screen(self.w, self.l)

        nodes = self.graph.get_vertices()
        self.k = math.sqrt(1 / len(nodes))

        self.c1 = 2
        self.c2 = 1
        self.c4 = .001

    def randomized_node_positions(self):
        for v in self.graph.get_vertices():
            x = random.random()
            y = random.random()
            self.positions[v] = Vector(x, y)

    def calc_repulsive_force(self, d):
        return (self.k ** 2 / d) * self.c1

    def calc_attractive_force(self, d):
        return (d ** 2 / self.k) * self.c2

    def iterate(self):

        movement = {}
        # Repulsive force between nodes
        for u in self.graph.get_vertices():
            movement[u] = Vector(0, 0)
            for v in self.graph.get_vertices():
                if u == v:
                    continue
                r = self.positions[u] - self.positions[v]
                dist = r.distance()
                if dist != 0:
                    f = self.calc_repulsive_force(dist) / dist
                    movement[u] = movement[u] + (r * f)

        # Attractive force between edges
        for (u, v) in self.graph.get_edges():
            r = self.positions[u] - self.positions[v]
            dist = r.distance()
            if dist != 0:
                f = self.calc_attractive_force(dist) / dist
                f = f * self.c4
                dd = r * f
                movement[u] = (movement[u] - dd)
                movement[v] = (movement[v] + dd)

        for v in self.graph.get_vertices():
            r = movement[v]
            dist = r.distance()
            if dist != 0:
                d = min(dist, self.t) / dist
                new_position = self.positions[v] + (r * d)
                self.positions[v].x = min(self.w/2, max(-self.w/2, new_position.x))
                self.positions[v].y = min(self.l/2, max(-self.l/2, new_position.y))
        self.t = self.t - .0001

    def run(self):
        self.randomized_node_positions()
        for i in range(0, 1000):
            self.iterate()
            self.screen.draw_graph(self.graph, self.positions)
            time.sleep(0.2)
        self.screen.wait_close()