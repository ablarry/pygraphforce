
from algorithms.spring import Spring
from pygraph import models

if __name__ == '__main__':
    g = models.mesh(10, 10)
    spring = Spring(g)
    spring.run()