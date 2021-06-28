import pygame

from pygraph import models
from algorithms.fruchterman import Fruchterman
if __name__ == '__main__':
    g = models.mesh(10,10)
    f = Fruchterman(g)
    f.run()