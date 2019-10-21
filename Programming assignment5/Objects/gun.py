import math;
from Objects.objects import *;

class Gun:
    def __init__(self, view_matrix, x, y, z):
        self.u = view_matrix.u;
        self.v = view_matrix.v;
        self.n = view_matrix.n;
        self.coordinates = view_matrix.eye + self.n * -0.5;
        self.view_matrix = view_matrix;

        self.rotation = -1.0;

    def set_translation(self, view_matrix, x, y, z):
        #self.location = Vector(x + 1, y - 0.7, z - 2.5);
        self.u = view_matrix.u;
        self.v = view_matrix.v;
        self.n = view_matrix.n;
        self.coordinates = view_matrix.eye + self.n * -0.5;

    def set_rotation(self, speed):
        self.rotation += speed;

    def get_transformations(self, view_matrix):
        return [{
                'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
                'translation': {'x': self.coordinates.xPos, 'y': self.coordinates.yPos - 1.0,
                                'z': self.coordinates.zPos},
                'scale': {'x': 1.0, 'y': 0.5, 'z': 3.0},
                'rotation': {'x': 0.0, 'y': self.rotation, 'z': 0.0}
            },
        ]


class Bullet:
    def __init__(self, view_matrix):
        self.u = view_matrix.u;
        self.v = view_matrix.v;
        self.n = view_matrix.n;

        self.location = view_matrix.eye;

        self.bullet_speed = 50;

    def update_movement(self, delta_time):
        self.location += self.n * -delta_time * self.bullet_speed;

    def get_transformations(self):
        return{
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos - 1.0,
                            'z': self.location.zPos},
            'scale': {'x': 0.5, 'y': 0.5, 'z': 0.5},
            'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}
        };


