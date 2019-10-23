import math;
from Objects.objects import *;

class Gun:
    def __init__(self, view_matrix, x, y, z):
        self.n = view_matrix.n;
        self.coordinates = view_matrix.eye + self.n * -0.5;

        self.rotation = -1.0;

    def set_translation(self, view_matrix, x, y, z):
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
        self.location = view_matrix.eye;
        self.n = view_matrix.n;

        self.bullet_speed = 50;

    def update_movement(self, delta_time):
        self.location += self.n * -delta_time * self.bullet_speed;

    def get_transformations(self):
        return{
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos - 1,
                            'z': self.location.zPos},
            'scale': {'x': 0.5, 'y': 0.5, 'z': 0.5},
            'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}
        };

    def wall_collision_check(self, wall_list, enemy_list):
        for wall in wall_list:
            trans = wall['translation'];
            scale = wall['scale'];
            rotation = wall['rotation'];

            if(rotation['y'] == 0.0):
                if(trans['x'] - scale['x'] / 2 < self.location.xPos < trans['x'] + scale['x'] / 2):
                    if(trans['z'] - scale['z'] / 2 < self.location.zPos < trans['z'] + scale['z'] / 2):
                        return True;
            else:
                if(trans['z'] - scale['x'] / 2 < self.location.zPos < trans['z'] + scale['x'] / 2):
                    if(trans['x'] - scale['z'] / 2 < self.location.xPos < trans['x'] + scale['z'] / 2):
                        return True;

        for i in enemy_list:
            wall = i.get_transformations();
            trans = wall['translation'];
            scale = wall['scale'];
            rotation = wall['rotation'];

            if(trans['x'] - scale['x'] / 2 < self.location.xPos < trans['x'] + scale['x'] / 2):
                if(trans['z'] - scale['z'] / 2 < self.location.zPos < trans['z'] + scale['z'] / 2):
                    print('YE')
                    return True;



