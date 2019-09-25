from OpenGL.GL import *;
import pygame;
import math;

from Shaders.shaders import *;
from Matrix.matrix import *;

screen_size = (800, 600);

class Game:
    def __init__(self):
        self.init_game();
        self.init_controls();

        self.shader = Shader3D();
        self.shader.render();

        self.model_matrix = Model_Matrix();
        self.view_matrix = View_Matrix();
        self.projection_matrix = Projection_Matrix();

        self.view_matrix.view(Point(3, 3, 3), Point(0, 0, 0), Vector(0, 1, 0));
        self.projection_matrix.set_perspective(math.pi / 2, screen_size[0] / screen_size[1], 0.5, 100);

        self.shader.set_view_matrix(self.view_matrix.get_matrix());
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());

        self.field_of_view = math.pi / 2;

        self.clock = pygame.time.Clock();
        self.clock.tick();

        self.cube = Cube();
        self.player_speed = 5;

        self.game_over = False;

        self.angle = 0;

    def update(self):
        delta_time = self.clock.tick() / 1000;

        self.angle += math.pi * delta_time;

        if(self.w_key_pressed):
            self.view_matrix.slide(0, 0, -self.player_speed * delta_time);
        if(self.s_key_pressed):
            self.view_matrix.slide(0, 0, self.player_speed * delta_time);

    def display(self):
        glEnable(GL_DEPTH_TEST);
        #glDisable(GL_DEPTH_TEST);
        glClearColor(0.0, 0.0, 1.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glViewport(0, 0, screen_size[0], screen_size[1]);

        self.projection_matrix.set_perspective(self.field_of_view, screen_size[0] / screen_size[1], 0.5, 100);
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());
        self.shader.set_view_matrix(self.view_matrix.get_matrix());
        self.model_matrix.reset_matrix();
        self.cube.set_cube_vertices(self.shader);

        self.draw_level();

        pygame.display.flip();

    def draw_level(self):
        ############ Wall 1
        self.shader.set_solid_color(1.0, 0.0, 1.0);

        self.model_matrix.push_matrix();
        #self.model_matrix.add_translation(0.0, 3.0, 0.0)
        self.model_matrix.add_scaling(3.0, 3.0, 3.0);
        self.model_matrix.add_rotation_y(self.angle)

        self.shader.set_model_matrix(self.model_matrix.get_model_matrix());
        self.cube.draw_cube();

        self.model_matrix.pop_matrix();
        #################################

    def game_loop(self):
        while not self.game_over:
            self.input_handler();
            self.update();
            self.display();

    def input_handler(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.game_over = True;

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_w):
                    self.w_key_pressed = True;
                elif(event.key == pygame.K_s):
                    self.s_key_pressed = True;

                if(event.key == pygame.K_a):
                    self.a_key_pressed = True;
                elif(event.key == pygame.K_d):
                    self.d_key_pressed = True;

            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_w):
                    self.w_key_pressed = False;
                elif(event.key == pygame.K_s):
                    self.s_key_pressed = False;

                if(event.key == pygame.K_a):
                    self.a_key_pressed = False;
                elif(event.key == pygame.K_d):
                    self.d_key_pressed = False;


    def init_game(self):
        pygame.init();
        pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF);

    def init_controls(self):
        self.w_key_pressed = False;
        self.a_key_pressed = False;
        self.s_key_pressed = False;
        self.d_key_pressed = False;

def main():
    game = Game();
    game.game_loop();

if __name__ == '__main__':
    main();