import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
from random import *


going_left = False;
x_pos = 100;


def init_game():
    pygame.display.init();
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL);

    glClearColor(0.0, 0.0, 1.0, 1.0);


def update():
    global x_pos;
    global going_left;

    if(going_left):
        x_pos -= 0.5;


def display():
    glClear(GL_COLOR_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glViewport(0, 0, 800, 600);
    gluOrtho2D(0, 800, 0, 600);

    glBegin(GL_TRIANGLES);
    glVertex2f(x_pos, 100);
    glVertex2f(x_pos, 200);
    glVertex2f(x_pos + 100, 100);
    glColor3f(1.0, 0.0, 1.0);
    glEnd();

    pygame.display.flip();


def game_loop():
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            quit();

        elif(event.type == pygame.KEYDOWN):
            if(event.key == K_ESCAPE):
                pygame.quit();
                quit();
            elif(event.key == K_q):
                glClearColor(random(), random(), random(), 1.0);

            elif(event.key == K_LEFT):
                going_left = True;

        elif(event.type == pygame.KEYUP):
            if(event.key == K_LEFT):
                going_left = False;

    update();
    display();


if __name__ == '__main__':
    init_game()
    while True:
        game_loop()