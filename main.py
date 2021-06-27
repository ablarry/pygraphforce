import pygame

from pygraph import models
from algorithms.Fruchterman import Fruchterman
if __name__ == '__main__':
    g = models.erdos_rengy(100, 150)
    f = Fruchterman(g)
    f.run()
