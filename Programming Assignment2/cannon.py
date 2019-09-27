from OpenGL.GL import *
from OpenGL.GLU import *
import math;

from vectors import *;


class Cannon:
    def __init__(self, x, y, obstacle_list, goal):
        self.x = x;
        self.y = y;
        self.angle = -45;

        self.rotating = False;
        self.rotation_direction = 0;

        self.cannon_ball = None;

        self.position = Point(x, y);
        #self.motion = Vector(x, y);

        self.obstacle_list = obstacle_list;
        self.goal = goal;


    def update_cannon(self, delta_time):
        if(self.rotating):
            self.rotate_cannon();

        if(self.cannon_ball != None):
            location = self.cannon_ball.get_location();
            if(location[0] > 800 or location[0] < 0 or location[1] < 0 or location[1] > 800):
                self.cannon_ball = None;
            else:
                self.cannon_ball.update(delta_time);


    def draw_cannon(self):
        glPushMatrix();

        glTranslate(self.position.x, self.position.y, 0);
        glColor3f(0.0, 0.0, 0.0);

        # Draw the platform for the cannon
        glBegin(GL_QUADS);
        glVertex2f(-50, 0);
        glVertex2f(-50, 20);
        glVertex2f(50, 20);
        glVertex2f(50, 0);
        glEnd();

        glPopMatrix();
        glPushMatrix();

        glTranslate(self.position.x, self.position.y, 0);
        glRotate(self.angle, 0, 0, 1);
        glTranslate(-self.position.x, -self.position.y, 0);
        glColor3f(0.0, 0.0, 0.0);

        # Draw the cannon itself
        glBegin(GL_QUADS);
        glVertex2f(0, 0);
        glVertex2f(0, 100);
        glVertex2f(20, 100);
        glVertex2f(20, 0);
        glEnd();

        glPopMatrix();

        if (self.cannon_ball != None):
            self.cannon_ball.draw_cannon_ball();


    def start_rotation(self, direction):
        self.rotating = True;
        self.rotation_direction = direction;


    def stop_rotation(self):
        self.rotating = False;
        self.rotation_direction = 0;


    def rotate_cannon(self):
        if(-90 <= self.angle + 0.1 * self.rotation_direction <= 0):
            self.angle += 0.1 * self.rotation_direction;


    def fire_cannon(self):
        if(self.cannon_ball == None):
            self.cannon_ball = Cannon_Ball(
                self.x, self.y, math.cos(self.angle * math.pi / 180),
                self.obstacle_list, self.goal
            );


    def set_obstacles(self, obstacle_list):
        self.obstacle_list = obstacle_list;
        self.cannon_ball = None;


class Cannon_Ball:
    def __init__(self, x, y, angle, obstacle_list, goal):
        self.position = Point(x, y)
        self.motion = Vector(x, y);

        self.x_direction = 1;
        self.y_direction = 1;

        self.angle = angle;
        self.obstacle_list = obstacle_list;
        self.goal = goal;


    def update(self, delta_time):
        for obst in self.obstacle_list:
            if (obst.check_collision_y(self.position, self.motion.y, self.y_direction)):
                self.y_direction *= -1;
            elif(obst.check_collision_x(self.position, self.motion.x, self.x_direction)):
                self.x_direction *= -1;


        self.goal.check_collision(self)

        self.motion.x += 500 * delta_time * self.x_direction * math.cos(self.angle);
        self.motion.y += 500 * delta_time * self.y_direction * math.sin(self.angle);
        self.position = self.motion;


    def draw_cannon_ball(self):
        # Inspired by an answer on this question:
        # https://stackoverflow.com/questions/17258546/opengl-creating-a-circle-change-radius

        glPushMatrix();
        glColor3f(1.0, 0.0, 1.0);
        glBegin(GL_POLYGON);

        for i in range(0, 100):
            x = 10 * math.cos(i * 2 * math.pi / 32) + self.position.x;
            y = 10 * math.sin(i * 2 * math.pi / 32) + self.position.y;

            glVertex2f(x, y);


        glEnd();
        glPopMatrix();


    def get_location(self):
        return (self.position.x, self.position.y);
