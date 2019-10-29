import math;
from Objects.objects import *;

class Gun:
    def __init__(self, model, bullet_model, view_matrix, x, y, z):
        self.model = model;
        self.bullet_model = bullet_model;
        self.n = view_matrix.n;
        self.coordinates = Vector(view_matrix.eye.xPos, view_matrix.eye.yPos - 1.0, view_matrix.eye.zPos - 2.5)

        self.rotation = -1.0;

    def player_move_x(self, speed):
        self.coordinates.xPos -= speed;

    def player_move_y(self, speed):
        self.coordinates.yPos += speed;

    def player_move_z(self, speed):
        self.coordinates.zPos -= speed;

    def set_translation(self, view_matrix):
        self.coordinates = Vector(view_matrix.eye.xPos - 2, view_matrix.eye.yPos - 1.0,
                                  view_matrix.eye.zPos - 1.5)
        self.rotate_gun(view_matrix);

    def set_rotation(self, speed):
        self.rotation += speed;

    def rotate_gun(self, view_matrix):
        eye = view_matrix.eye;
        angle = -self.rotation;

        x = math.cos(angle) * (self.coordinates.xPos - eye.xPos) \
            - math.sin(angle) * (self.coordinates.zPos - eye.zPos) + eye.xPos;

        z = math.sin(angle) * (self.coordinates.xPos - eye.xPos) \
            + math.cos(angle) * (self.coordinates.zPos - eye.zPos) + eye.zPos;

        self.coordinates.xPos = x;
        self.coordinates.zPos = z;

    def fire_gun(self, view_matrix):
        return Bullet(self.bullet_model, view_matrix, self.rotation);

    def get_model(self):
        return self.model;

    def get_transformations(self):
        return {
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.coordinates.xPos, 'y': self.coordinates.yPos,
                            'z': self.coordinates.zPos},
            'scale': {'x': 20.0, 'y': 20.0, 'z': 20.0},
            'rotation': {'x': 0.0, 'y': self.rotation + 2 * math.pi/2, 'z': 0.0}
        };


class Bullet:
    def __init__(self, model, view_matrix, rotation):
        self.model = model;
        self.location = view_matrix.eye;
        self.n = view_matrix.n;

        self.rotation = rotation;

        self.bullet_speed = 200;

    def update_movement(self, delta_time):
        self.location += self.n * -delta_time * self.bullet_speed;

    def get_model(self):
        return self.model;

    def get_transformations(self):
        return{
            'color': {'r': 0.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos - 1,
                            'z': self.location.zPos},
            'scale': {'x': 100.0, 'y': 100.0, 'z': 100.0},
            'rotation': {'x': 0.0, 'y': self.rotation - math.pi/2, 'z': math.pi / 2}
        };

    def wall_collision_check(self, wall_list):
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

    def enemy_collision_check(self, enemy_list):
        for i in enemy_list:
            enemy = i.get_transformations();
            trans = enemy['translation'];
            scale = enemy['scale'];

            if(trans['x'] - scale['x'] / 2 < self.location.xPos < trans['x'] + scale['x'] / 2):
                if(trans['z'] - scale['z'] / 2 < self.location.zPos < trans['z'] + scale['z'] / 2):
                    i.damage_enemy();
                    return True;