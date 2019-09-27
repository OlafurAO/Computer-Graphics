import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Vector:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y);

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other);


class Point:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y);

position = Point(100, 100);
motion = Vector(0, 0);


def init_game():
    pygame.display.init();
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL);

    glClearColor(0.0, 0.0, 1.0, 1.0);


def update():
    pass;


def display():
    pass;


def main():
    init_game();

    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit();
                quit();

if __name__ == '__main__':
    main();