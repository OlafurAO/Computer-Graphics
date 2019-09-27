import pygame;
from pygame.locals import *;

from OpenGL.GL import *;
from OpenGL.GLU import *;

import random;
from random import *;

screen_size = (800, 600);

class Box:
    def __init__(self, location):
        self.location = location;
        self.direction_x = 1;
        self.direction_y = -1;

        self.color_r = random();
        self.color_g = random();
        self.color_b = random();

    def draw_box(self):
        glBegin(GL_QUADS);
        glVertex2f(self.location[0], self.location[1]);
        glVertex2f(self.location[0], self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1]);
        glColor3f(self.color_r, self.color_g, self.color_b);
        glEnd();

    def update_position(self):
        self.location[0] += self.direction_x * 0.2;
        self.location[1] += self.direction_y * 0.2;

    def edge_collision_check(self):
        if(self.location[0] <= 0):
            self.direction_x = 1;
            self.change_color();
        elif(self.location[0] >= screen_size[0] - 50):
            self.direction_x = -1;
            self.change_color();

        if(self.location[1] <= 0):
            self.direction_y = 1;
            self.change_color();
        elif(self.location[1] >= screen_size[1] - 50):
            self.direction_y = -1;
            self.change_color();

    def change_color(self):
        self.color_r = random();
        self.color_g = random();
        self.color_b = random();


def init_game():
    pygame.display.init();
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL);
    glClearColor(0.0, 0.0, 1.0, 1.0);


def update(box):
    box.edge_collision_check();
    box.update_position();


def display(box):
    glClear(GL_COLOR_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glViewport(0, 0, 800, 600);
    gluOrtho2D(0, 800, 0, 600);

    box.draw_box();

    pygame.display.flip();


def main():
    init_game();
    box = Box([screen_size[0] / 2, screen_size[1] / 2]);

    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit();
                quit();

        update(box);
        display(box);

if __name__ == '__main__':
    main();