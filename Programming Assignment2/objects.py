from OpenGL.GL import *
from OpenGL.GLU import *

from random import *;

from vectors import *;

class Goal:
    def __init__(self, screen_size):
        self.screen_size = screen_size;
        self.position = self.set_point();
        self.goal_score = False;

        self.width = 50;
        self.height = 50;


    def set_point(self):
        return Point(randrange(300, self.screen_size[0] - 100), randrange(200, self.screen_size[1] - 100));


    def draw_goal(self):
        glPushMatrix();

        glTranslate(self.position.x, self.position.y, 0);
        glColor3f(0.0, 0.7, 0);

        glBegin(GL_TRIANGLE_STRIP);
        glVertex2f(0, 0);
        glVertex2f(0, 50);
        glVertex2f(50, 50);
        glVertex2f(50, 0);
        glEnd();

        glPopMatrix();


    def check_collision(self, cannon_ball):
        if(self.check_collision_x(cannon_ball) and self.check_collision_y(cannon_ball)):
            self.position = self.set_point();
            self.goal_score = True;
            return True;


    def check_collision_x(self, cannon_ball):
        return cannon_ball.position.x + 10 >= self.position.x and \
                      self.position.x + self.width >= cannon_ball.position.x;


    def check_collision_y(self, cannon_ball):
        return cannon_ball.position.y + 10 >= self.position.y and \
                      self.position.y + self.height >= cannon_ball.position.y


class Box:
    def __init__(self, position, screen_height):
        self.width = 1;
        self.height = 1;

        self.position = Point(position[0], screen_height - position[1])
        self.initial_mouse_pos = position;

        self.height_multiplier = 1;


    def draw_obstacle(self):
        glPushMatrix();

        glTranslate(self.position.x, self.position.y, 0);
        glColor3f(1.0, 0.0, 0.0);

        glBegin(GL_QUADS);
        glVertex2f(0, 0);
        glVertex2f(0, self.height);
        glVertex2f(self.width, self.height);
        glVertex2f(self.width, 0);
        glEnd();

        glPopMatrix();


    def resize_obstacle(self, mouse_position):
        self.width = mouse_position[0] - self.initial_mouse_pos[0];
        self.height = self.initial_mouse_pos[1] - mouse_position[1];

        if(self.height < 0):
            self.height_multiplier = -1;
        else:
            self.height_multiplier = 1;


    def check_collision_x(self, cannon_ball_pos, motion_x, x_direction):
        if(self.position.x <= cannon_ball_pos.x + (cannon_ball_pos.x - motion_x) + 10 * x_direction <= self.position.x + self.width):
            if(self.position.y - 10 >= cannon_ball_pos.y >= self.position.y - self.height * self.height_multiplier):
                return True;


    def check_collision_y(self, cannon_ball_pos, motion_y, y_direction):
        if(self.position.y >= cannon_ball_pos.y + (cannon_ball_pos.y - motion_y) + 10 * y_direction >=
                   self.position.y - self.height * self.height_multiplier):
            if(self.position.x <= cannon_ball_pos.x <= self.position.x + self.width):
                return True;


    def get_position(self):
        return self.position;


class Line:
    def __init__(self, position, screen_height):
        self.position = Point(position[0], screen_height - position[1])
        self.length_x = 0;
        self.length_y = 0;

        self.initial_position = position;

        self.screen_height = screen_height;


    def draw_obstacle(self):
        glPushMatrix();

        glTranslate(self.position.x, self.position.y, 0);
        glColor3f(1.0, 0.0, 0.0);

        glBegin(GL_LINES);
        glVertex2f(0, 0);
        glVertex2f(self.length_x, self.length_y)
        glEnd();

        glPopMatrix();


    def resize_obstacle(self, mouse_position):
        self.length_x = mouse_position[0] - self.initial_position[0];
        self.length_y = self.initial_position[1] - mouse_position[1]


    def check_collision_x(self, cannon_ball_pos, motion_x, x_direction):
        return False;


    def check_collision_y(self, cannon_ball_pos, motion_y, y_direction):
        return False;