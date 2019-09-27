import pygame;
from pygame.locals import *;

from OpenGL.GL import *;
from OpenGL.GLU import *;

screen_size = (800, 600);

class Box:
    def __init__(self, location):
        self.location = location;
        self.direction_x = 1;
        self.direction_y = 1;

        self.is_moving_x = False;
        self.is_moving_y = False;


    def draw_box(self):
        glBegin(GL_QUADS);
        glVertex2f(self.location[0], self.location[1]);
        glVertex2f(self.location[0], self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1] + 50);
        glVertex2f(self.location[0] + 50, self.location[1]);
        glColor3f(1.0, 0.0, 1.0);
        glEnd();


    def update_box(self):
        if(self.is_moving_x):
            self.move_box_x();
        if(self.is_moving_y):
            self.move_box_y();


    def move_input_x(self, direction):
        if(direction != 0):
            self.is_moving_x = True;
            self.direction_x = direction;
        else:
            self.is_moving_x = False;


    def move_input_y(self, direction):
        if(direction != 0):
            self.is_moving_y = True;
            self.direction_y = direction;
        else:
            self.is_moving_y = False;


    def move_box_x(self):
        next_location = self.location[0] + self.direction_x * 0.5;
        if not(self.edge_collision_check_x(next_location)):
            self.location[0] += self.direction_x * 0.5;


    def move_box_y(self):
        next_location = self.location[1] + self.direction_y * 0.5;
        if not(self.edge_collision_check_y(next_location)):
            self.location[1] += self.direction_y * 0.5;


    def edge_collision_check_x(self, next_location):
        return next_location >= screen_size[0] - 50 or next_location <= 0


    def edge_collision_check_y(self, next_location):
        return next_location >= screen_size[1] - 50 or next_location <= 0;


def init_game():
    pygame.display.init();
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL);
    glClearColor(0.0, 0.0, 1.0, 1.0);


def update(box):
    box.update_box();
    pass


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

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    box.move_input_x(-1);
                elif(event.key == pygame.K_RIGHT):
                    box.move_input_x(1);

                if(event.key == pygame.K_UP):
                    box.move_input_y(1);
                elif(event.key == pygame.K_DOWN):
                    box.move_input_y(-1);

            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_LEFT):
                    box.move_input_x(0);
                if(event.key == pygame.K_RIGHT):
                    box.move_input_x(0);

                if(event.key == pygame.K_UP):
                    box.move_input_y(0);
                if(event.key == pygame.K_DOWN):
                    box.move_input_y(0);

        update(box);
        display(box);


if __name__ == '__main__':
    main();