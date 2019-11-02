from Objects.objects import *;
import math;

class Enemy:
    def __init__(self, model, texture, color, trans, scale, rotation, width):
        self.model = model;
        self.texture = texture;
        self.color = color;
        self.location = Vector(trans[0], trans[1], trans[2]);
        self.scale = scale;
        self.rotation = list(rotation);
        self.width = width;

        self.health = 5;
        self.speed = 0.03;

        self.death_rotation = 0.0;
        self.death_timer = 0;

        self.enemy_dying = False;
        self.enemy_dead = False;
        self.aggroed = False;

    def set_translation(self, player_view_matrix, wall_list):
        eye = player_view_matrix.eye;
        distance = self.get_distance_to_player(eye);

        if(distance < 40 or self.aggroed):
            if(eye.xPos >= self.location.xPos + 1):
                self.location.xPos += self.speed;
            elif(eye.xPos <= self.location.xPos - 1):
                self.location.xPos -= self.speed;

            if(eye.zPos >= self.location.zPos + 1):
                self.location.zPos += self.speed;
            elif(eye.zPos <= self.location.zPos - 1):
                self.location.zPos -= self.speed;

        if(self.is_dying()):
            if(self.death_timer == 0 and not self.enemy_dying):
                self.death_timer = 120;
                self.enemy_dying = True;
            if(self.death_timer > 0):
                self.death_timer -= 1;
                self.death_rotation -= 0.01;
            else:
                self.enemy_dead = True;

    def set_rotation(self, player_view_matrix):
        eye = player_view_matrix.eye;

        angle = (eye.zPos - self.location.zPos) / (eye.xPos - self.location.xPos);
        self.rotation[1] = math.atan(-angle);

    def damage_enemy(self, damage):
        self.health -= damage;
        print(self.health)

        if not(self.aggroed):
            self.aggroed = True;

    def get_transformations(self):
        return {
            'color': {'r': self.color[0], 'g': self.color[1], 'b': self.color[2]},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos - 1.5,
                            'z': self.location.zPos},
            'scale': {'x': self.scale[0], 'y': self.scale[1], 'z': self.scale[2]},
            'rotation': {'x': -self.death_rotation, 'y': self.rotation[1] + math.pi/2,
                         'z': self.rotation[2]}
        };

    def get_location(self):
        return self.location;

    def get_model(self):
        return self.model;

    def get_texture(self):
        return self.texture;

    def get_distance_to_player(self, eye):
        return math.sqrt((eye.xPos - self.location.xPos) ** 2
                         + (eye.zPos - self.location.zPos) ** 2);

    def get_width(self):
        return self.width;

    def is_dead(self):
        return self.enemy_dead;

    def is_dying(self):
        return self.health <= 0;