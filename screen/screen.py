import pygame

from screen.vector import Vector


class Screen:
    def __init__(self, width=1000, height=1000):
        self.width = width
        self.height = height
        self.screen_size = Vector(width, height)
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size.point())
        self.node_color = 255, 0, 0
        self.node_border_color = 0, 0, 0
        self.node_border_thickness = 2
        self.node_radius = 5
        self.line_color = 0, 0, 0
        self.line_thickness = 1
        self.background_color = 255, 255, 255
        self.screen.fill(self.background_color)
        pygame.display.update()

    def draw_point(self, coordinate):
        point = coordinate.point()
        pygame.draw.circle(self.screen, self.node_color, point, self.node_radius)
        pygame.draw.circle(self.screen, self.node_border_color, point, self.node_radius, self.node_border_thickness)

    def draw_line(self, origin, end):
        pygame.draw.line(self.screen, self.line_color, origin.point(), end.point(), self.line_thickness)

    def linear_transformation(self, positions):
        # Find maxX and minX
        x_max = max(positions[p].x for p in positions)
        x_min = min(positions[p].x for p in positions)

        # Find maxY and minY
        y_max = max(positions[p].y for p in positions)
        y_min = min(positions[p].y for p in positions)

        # Calculate scala_x
        scala_x = (self.width - (self.width/2)) / (x_max - x_min)
        # Calculate scala_y
        scala_y = (self.height - (self.height/2)) / (y_max - y_min)

        new_positions = {}
        for p in positions:
            new_x = (scala_x * positions[p].x) + ((self.width/2) - x_min)
            new_y = (scala_y * positions[p].y) + ((self.height/2) - y_min)
            new_positions[p] = Vector(new_x, new_y)

        return new_positions

    def draw_graph(self, graph, positions):

        new_positions = self.linear_transformation(positions)
        self.screen.fill(self.background_color)
        for e in graph.get_edges():
            (o, s) = e
            # origin = positions[o] * self.screen_size
            # end = positions[s] * self.screen_size
            origin = new_positions[o]
            end = new_positions[s]
            self.draw_line(origin, end)

        for v in graph.get_vertices():
            # coordinate = positions[v] * self.screen_size
            coordinate = new_positions[v]
            self.draw_point(coordinate)
        pygame.display.update()

    def wait_close(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
