from OpenGL.GL import *;
import pygame;
import math;

from Shaders.shaders import *;
from Matrix.matrix import *;

screen_size = (1200, 800);

class Game:
    def __init__(self):
        self.init_game();
        self.init_controls();

        self.shader = Shader3D();
        self.shader.render();

        self.model_matrix = Model_Matrix();
        self.view_matrix = View_Matrix();
        self.projection_matrix = Projection_Matrix();

        self.view_matrix.view(Point(3, 0, 3), Point(0, 0, 0), Vector(0, 1, 0));
        self.projection_matrix.set_perspective(math.pi / 2, screen_size[0] / screen_size[1], 0.5, 100);

        self.shader.set_view_matrix(self.view_matrix.get_matrix());
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());

        self.field_of_view = math.pi / 2;

        self.clock = pygame.time.Clock();
        self.clock.tick();
        self.delta_time = self.clock.tick() / 1000;

        self.cube = Cube();

        self.mouse_sensitivity = 5;
        self.player_speed = 5;
        self.angle = 0;

        self.game_over = False;

    def update(self):
        self.delta_time = self.clock.tick() / 1000;
        self.angle += math.pi * self.delta_time;
        self.mouse_pos = list(pygame.mouse.get_pos());

        ###############Keyboard controls
        if(self.w_key_pressed):
            self.view_matrix.slide(0, 0, -self.player_speed * self.delta_time);
        elif(self.s_key_pressed):
            self.view_matrix.slide(0, 0, self.player_speed * self.delta_time);

        if(self.a_key_pressed):
            self.view_matrix.slide(self.player_speed * self.delta_time, 0, 0);
        elif(self.d_key_pressed):
            self.view_matrix.slide(-self.player_speed * self.delta_time, 0, 0);

        ###############Reset mouse position
        if(self.mouse_pos[0] < 100):
            pygame.mouse.set_pos(screen_size[0] / 2, self.mouse_pos[1])
            self.mouse_pos[0] = screen_size[0] / 2;
        elif(self.mouse_pos[0] > screen_size[0] - 100):
            pygame.mouse.set_pos(screen_size[0] / 2, self.mouse_pos[1])
            self.mouse_pos[0] = screen_size[0] / 2;

        if(self.mouse_pos[1] < 100):
            pygame.mouse.set_pos(self.mouse_pos[0], screen_size[1] / 2);
            self.mouse_pos[1] = screen_size[1] / 2;
        elif(self.mouse_pos[1] > screen_size[1] - 100):
            pygame.mouse.set_pos(self.mouse_pos[0], screen_size[1] / 2);
            self.mouse_pos[1] = screen_size[1] / 2;

    def display(self):
        glEnable(GL_DEPTH_TEST);
        #glDisable(GL_DEPTH_TEST);
        glClearColor(0.0, 0.0, 1.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glViewport(0, 0, screen_size[0], screen_size[1]);

        self.projection_matrix.set_perspective(self.field_of_view, screen_size[0] / screen_size[1], 0.5, 100);
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());
        self.shader.set_view_matrix(self.view_matrix.get_matrix());
        self.model_matrix.load_identity();
        self.cube.set_cube_vertices(self.shader);

        self.draw_level();

        pygame.display.flip();

    def draw_level(self):
        ############ Wall 1
        color = {'r': 1.0, 'g': 0.0, 'b': 1.0};
        translation = {'x': 0.0, 'y': 0.0, 'z': -7.0}
        scale = {'x': 15.0, 'y': 3.0, 'z': 1.0};
        rotation_angle = {'x': 0.0, 'y': 0.0, 'z': 0.0};

        self.draw_cube(color, translation, scale, rotation_angle);
        #################################
        ############ Wall 2
        color = {'r': 0.0, 'g': 1.0, 'b': 1.0};
        translation = {'x': 8.0, 'y': 0.0, 'z': 0.0}
        scale = {'x': 15.0, 'y': 3.0, 'z': 1.0};
        rotation_angle = {'x': 0.0, 'y': 4.75, 'z': 0.0};

        self.draw_cube(color, translation, scale, rotation_angle);
        #################################
        '''
        ############ Wall 3
        color = {'r': 0.0, 'g': 1.0, 'b': 0.0};
        translation = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        scale = {'x': 1.0, 'y': 1.0, 'z': 2.0};
        rotation_angle = {'x': 0.0, 'y': 4.4, 'z': 0.0};

        self.draw_cube(color, translation, scale, rotation_angle);
        #################################
        '''

    def draw_cube(self, color, trans, scale, rotation):
        self.shader.set_solid_color(color['r'], color['g'], color['b']);
        self.model_matrix.push_matrix();

        self.model_matrix.add_translation(trans['x'], trans['y'], trans['z']);

        self.model_matrix.add_rotation_x(rotation['x']);
        self.model_matrix.add_rotation_y(rotation['y']);
        self.model_matrix.add_rotation_z(rotation['z']);

        self.model_matrix.add_scaling(scale['x'], scale['y'], scale['z']);

        self.shader.set_model_matrix(self.model_matrix.get_model_matrix());
        self.cube.draw_cube();
        self.model_matrix.pop_matrix();

    def game_loop(self):
        while not self.game_over:
            self.input_handler();
            self.update();
            self.display();

    def input_handler(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.game_over = True;

            if(event.type == pygame.MOUSEMOTION):
                new_mouse_pos = pygame.mouse.get_pos();

                if(new_mouse_pos[0] > self.mouse_pos[0]):
                    mouse_x_pos_movement = new_mouse_pos[0] - self.mouse_pos[0];
                    self.view_matrix.yaw(self.delta_time * mouse_x_pos_movement);
                    self.mouse_pos = list(new_mouse_pos);
                elif(new_mouse_pos[0] < self.mouse_pos[0]):
                    mouse_x_pos_movement = self.mouse_pos[0] - new_mouse_pos[0];
                    self.view_matrix.yaw(-self.delta_time * mouse_x_pos_movement);
                    self.mouse_pos = list(new_mouse_pos);

                if(new_mouse_pos[1] > self.mouse_pos[1]):
                    mouse_y_pos_movement = self.mouse_pos[1] - new_mouse_pos[1];
                    self.view_matrix.pitch(self.delta_time * mouse_y_pos_movement);
                    self.mouse_pos = list(new_mouse_pos);
                elif(new_mouse_pos[1] < self.mouse_pos[1]):
                    mouse_y_pos_movement = new_mouse_pos[1] - self.mouse_pos[1];
                    self.view_matrix.pitch(-self.delta_time * mouse_y_pos_movement);
                    self.mouse_pos = list(new_mouse_pos);

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_q):
                    self.game_over = True;

                if(event.key == pygame.K_w):
                    self.w_key_pressed = True;
                elif(event.key == pygame.K_s):
                    self.s_key_pressed = True;

                if(event.key == pygame.K_a):
                    self.a_key_pressed = True;
                elif(event.key == pygame.K_d):
                    self.d_key_pressed = True;

                if(event.key == pygame.K_LSHIFT):
                    self.player_speed = 10;

            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_w):
                    self.w_key_pressed = False;
                elif(event.key == pygame.K_s):
                    self.s_key_pressed = False;

                if(event.key == pygame.K_a):
                    self.a_key_pressed = False;
                elif(event.key == pygame.K_d):
                    self.d_key_pressed = False;

                if (event.key == pygame.K_LSHIFT):
                    self.player_speed = 5;

    def init_game(self):
        pygame.init();
        pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF);
        pygame.mouse.set_cursor(
                (8, 8), (0, 0),
                (0, 0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0, 0)
        );

    def init_controls(self):
        self.mouse_pos = list(pygame.mouse.get_pos());
        self.tmp_mouse_pos = 0;
        self.mouse_move_up = False;
        self.mouse_move_down = False;
        self.mouse_move_left = False;
        self.mouse_move_right = False;

        self.w_key_pressed = False;
        self.a_key_pressed = False;
        self.s_key_pressed = False;
        self.d_key_pressed = False;

def main():
    game = Game();
    game.game_loop();

if __name__ == '__main__':
    main();