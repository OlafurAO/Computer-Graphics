from Objects.objects import *;


class Particle_Effect:
    def __init__(self, texture, position):
        self.texture = texture;
        self.position = position;

    def update(self, delta_time):
        pass

    def draw(self, shader):
        pass;