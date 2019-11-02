import math;
from Objects.objects import *;

class Health:
    def __init__(self, view_matrix):
        self.coordinates = Vector(view_matrix.eye.xPos, view_matrix.eye.yPos - 1.0,
                                  view_matrix.eye.zPos - 2.5)
        self.rotation = -1;

    def set_translation(self, view_matrix):
        self.coordinates = Vector(view_matrix.eye.xPos + 4, view_matrix.eye.yPos - 1.3,
                                  view_matrix.eye.zPos - 2.5)
        self.rotate_cube(view_matrix);

    def set_rotation(self, speed):
        self.rotation += speed;

    def rotate_cube(self, view_matrix):
        eye = view_matrix.eye;
        angle = -self.rotation;

        x = math.cos(angle) * (self.coordinates.xPos - eye.xPos) \
            - math.sin(angle) * (self.coordinates.zPos - eye.zPos) + eye.xPos;

        z = math.sin(angle) * (self.coordinates.xPos - eye.xPos) \
            + math.cos(angle) * (self.coordinates.zPos - eye.zPos) + eye.zPos;

        self.coordinates.xPos = x;
        self.coordinates.zPos = z;

    def get_transformations(self):
        return {
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.coordinates.xPos, 'y': self.coordinates.yPos,
                            'z': self.coordinates.zPos},
            'scale': {'x': 1.0, 'y': 20.0, 'z': 0.2},
            'rotation': {'x': 0.0, 'y': self.rotation - math.pi/2, 'z': 0.0}
        };

    def get_rotation(self):
        return self.rotation;