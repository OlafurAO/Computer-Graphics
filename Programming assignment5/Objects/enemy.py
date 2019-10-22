from Objects.objects import *;

class Enemy:
    def __init__(self, color, trans, scale, rotation):
        self.color = color;
        self.location = Vector(trans[0], trans[1], trans[2]);
        self.scale = scale;
        self.rotation = list(rotation);

        self.health = 5;

    def set_translation(self, player_view_matrix):
        pass

    def set_rotation(self, player_view_matrix):
        eye = player_view_matrix.eye;
        dot = self.location.xPos * eye.xPos \
            + self.location.yPos * eye.yPos \
            + self.location.zPos * eye.zPos;

        a = self.location.__len__();
        b = eye.__len__();

        angle = dot / (a * b);

        self.rotation[1] = angle;

    def get_transformations(self):
        return {
            'color': {'r': self.color[0], 'g': self.color[1], 'b': self.color[2]},
            'translation': {'x': self.location.xPos, 'y': self.location.yPos,
                            'z': self.location.zPos},
            'scale': {'x': self.scale[0], 'y': self.scale[1], 'z': self.scale[2]},
            'rotation': {'x': self.rotation[0], 'y': self.rotation[1],
                         'z': self.rotation[2]}
        };