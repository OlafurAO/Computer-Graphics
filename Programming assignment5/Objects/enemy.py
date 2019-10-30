from Objects.objects import *;
import math;

class Enemy:
    def __init__(self, model, color, trans, scale, rotation):
        self.model = model;
        self.color = color;
        self.location = Vector(trans[0], trans[1], trans[2]);
        self.scale = scale;
        self.rotation = list(rotation);

        self.health = 5;
        self.speed = 0.01;

        self.aggroed = False;

    def set_translation(self, player_view_matrix):
        eye = player_view_matrix.eye;
        distance = self.get_distance_to_player(eye);

        if(distance < 20 or self.aggroed):
            if(eye.xPos > self.location.xPos):
                self.location.xPos += self.speed;
            elif(eye.xPos < self.location.xPos):
                self.location.xPos -= self.speed;

            if(eye.zPos > self.location.zPos):
                self.location.zPos += self.speed;
            elif(eye.zPos < self.location.zPos):
                self.location.zPos -= self.speed;

    def set_rotation(self, player_view_matrix):
        eye = player_view_matrix.eye;

        angle = (eye.zPos - self.location.zPos) / (eye.xPos - self.location.xPos);
        self.rotation[1] = math.atan(-angle);

    def damage_enemy(self):
        self.health -= 1;
        self.color = [1.0, 0.0, 0.0];
        print(self.health)

        if not(self.aggroed):
            self.aggroed = True;

    def get_transformations(self):
        return {
            'color': {'r': self.color[0], 'g': self.color[1], 'b': self.color[2]},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos - 1.5,
                            'z': self.location.zPos},
            'scale': {'x': self.scale[0], 'y': self.scale[1], 'z': self.scale[2]},
            'rotation': {'x': self.rotation[0], 'y': self.rotation[1] + math.pi/2,
                         'z': self.rotation[2]}
        };

    def get_model(self):
        return self.model;

    def get_distance_to_player(self, eye):
        return math.sqrt((eye.xPos - self.location.xPos) ** 2
                         + (eye.zPos - self.location.zPos) ** 2);

    def is_dead(self):
        return self.health <= 0;