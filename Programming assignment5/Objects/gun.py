import math;
from Objects.objects import *;

class Gun:
    def __init__(self, model, bullet_model, texture, gunfire_sfx, damage, fire_rate, view_matrix, automatic):
        self.model = model;
        self.bullet_model = bullet_model;
        self.texture = texture;
        self.gunfire_sfx = gunfire_sfx;
        self.damage = damage;
        self.fire_rate = fire_rate;
        self.automatic = automatic;

        self.n = view_matrix.n;
        self.coordinates = Vector(view_matrix.eye.xPos, view_matrix.eye.yPos - 1.0,
                                  view_matrix.eye.zPos - 2.5)
        self.rotation = -1.0;
        self.rotation_x = 0.0;
        self.fire_timer = 0;
        self.fire_rate_timer = 0;

    def set_translation(self, view_matrix):
        self.coordinates = Vector(view_matrix.eye.xPos - 2, view_matrix.eye.yPos - 1.0,
                                  view_matrix.eye.zPos - 1.5)
        self.rotate_gun(view_matrix);

        if(self.fire_timer > 0):
            if(5 <= self.fire_timer <= 10):
                self.rotation_x += 0.1;
            else:
                self.rotation_x -= 0.1;

            self.fire_timer -= 1;
        else:
            self.cease_fire();

        if(self.fire_rate_timer > 0):
            self.fire_rate_timer -= 1;

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
        if(self.fire_rate_timer == 0):
            if(self.fire_timer == 0):
                self.fire_timer = 12;

            self.fire_rate_timer = self.fire_rate;
            self.gunfire_sfx.play();

            return Bullet(self.bullet_model, self.damage, view_matrix, self.rotation);

    def cease_fire(self):
        self.rotation_x = 0.0;

    def get_model(self):
        return self.model;

    def get_transformations(self):
        return {
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.coordinates.xPos, 'y': self.coordinates.yPos + self.rotation_x,
                            'z': self.coordinates.zPos},
            'scale': {'x': 20.0, 'y': 20.0, 'z': 20.0},
            'rotation': {'x': -self.rotation_x, 'y': self.rotation + 2 * math.pi/2, 'z': 0.0}
        };

    def get_fire_rate(self):
        return self.fire_rate;

    def is_automatic(self):
        return self.automatic;


class Reticule:
    def __init__(self, view_matrix):
        self.n = view_matrix.n;
        self.location = view_matrix.eye + self.n * -0.5;
        self.rotation = -1;

    def set_translation(self, view_matrix):
        self.n = view_matrix.n;
        self.location = view_matrix.eye + self.n * -1.5;

    def set_rotation(self, speed):
        self.rotation += speed;

    def get_transformations(self):
        return {
            'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos,
                            'z': self.location.zPos},
            'scale': {'x': 0.025, 'y': 0.025, 'z': 0.01},
            'rotation': {'x': 0.0, 'y': self.rotation, 'z': 0.0}
        };


class Bullet:
    def __init__(self, model, damage, view_matrix, rotation):
        self.model = model;
        self.damage = damage;
        self.location = view_matrix.eye + view_matrix.n * 0.01;
        self.n = view_matrix.n;

        self.rotation = rotation;

        self.bullet_speed = 200;

        # On automatic fire, some bullets go through the walls.
        # That's why after a certain amount of time, the bullets
        # are removed from the bullet list to prevent slowdown
        self.bullet_time = 0;

    def update_movement(self, delta_time):
        self.location += self.n * -delta_time * self.bullet_speed;
        self.bullet_time += 1;

    def get_model(self):
        return self.model;

    def get_transformations(self):
        return{
            'color': {'r': 0.0, 'g': 0.0, 'b': 0.0},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos,
                            'z': self.location.zPos},
            'scale': {'x': 100.0, 'y': 100.0, 'z': 100.0},
            'rotation': {'x': 0.0, 'y': self.rotation - math.pi/2, 'z': math.pi / 2}
        };

    def get_time(self):
        return self.bullet_time;

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
            width = i.get_width();

            if(trans['x'] - width / 2 < self.location.xPos < trans['x'] + width / 2):
                if(trans['z'] - width / 2 < self.location.zPos < trans['z'] + width / 2):
                    i.damage_enemy(self.damage);
                    return True;