import pygame

from algorithms.spring import Spring
from pygraph import models

if __name__ == '__main__':
    g = models.erdos_rengy(100, 200)
    spring = Spring(g)
    spring.run()
