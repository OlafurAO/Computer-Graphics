import pygame;
from pygame.locals import *;

from OpenGL.GL import *;
from OpenGL.GLU import *;

screen_size = (800, 600);

class Box:
    def __init__(self, location):
        self.location = list(location);
        self.location[0] -= 25;
        # OpenGL grid starts in the bottom left corner instead of the top right
        self.location[1] = screen_size[1] - self.location[1] - 25;


    def draw_box(self):
        glBegin(GL_QUADS);
        glVertex2f(self.location[0], self.location[1]);
        glVertex2f(self.location[0], self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1]);
        glColor3f(1.0, 0.0, 1.0);
        glEnd();


def init_game():
    pygame.display.init();
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL);
    glClearColor(0.0, 0.0, 1.0, 1.0);


def display(box_list):
    glClear(GL_COLOR_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glViewport(0, 0, 800, 600);
    gluOrtho2D(0, 800, 0, 600);

    for box in box_list:
        box.draw_box();

    pygame.display.flip();


def main():
    init_game();

    box_list = [];

    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit();
                quit();

            if(event.type == pygame.MOUSEBUTTONDOWN):
                box_list.append(Box(pygame.mouse.get_pos()));

        display(box_list);


if __name__ == '__main__':
    main();