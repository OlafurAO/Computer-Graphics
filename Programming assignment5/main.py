from OpenGL.GL import *;
from OpenGL.GLU import *
import pygame;
import math;
import sys;

from Shaders.shaders import *;
from Matrix.matrix import *;

screen_size = (1200, 800);

# NOTE: this game utilizes mouse controls and works best with an actual mouse, rather than a touchpad
class Game:
    def __init__(self):
        self.init_game();
        self.init_controls();
        self.init_level();

        self.shader = Shader3D();
        self.shader.render();

        self.model_matrix = Model_Matrix();
        self.view_matrix = View_Matrix();
        self.projection_matrix = Projection_Matrix();

        self.view_matrix.view(Point(-5, 0, 3), Point(0, 0, 0), Vector(0, 1, 0));
        self.projection_matrix.set_perspective(math.pi / 2, screen_size[0] / screen_size[1], 0.5, 100);

        self.shader.set_view_matrix(self.view_matrix.get_matrix());
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());

        self.field_of_view = math.pi / 2;

        self.clock = pygame.time.Clock();
        self.clock.tick();
        self.delta_time = self.clock.tick() / 1000;

        self.cube = Cube();

        self.mouse_sensitivity = 5;
        self.angle = 0;

        self.player_speed = 10;
        self.jump_speed = 10;
        self.jump_counter = 0;

        self.game_over = False;
        self.player_sprinting = False;

        self.player_direction = 0;
        self.player_collision_direction = None;

        self.tex_id01 = self.load_texture_3D('/Assets/Art/test.jpg');
        self.tex_id02 = self.load_texture_3D('/Assets/Art/doom_spritesheet.png');

        self.sprite = self.load_texture_2D('/Assets/Art/Spritesheets/Player/tile000.png');


    def update(self):
        self.delta_time = self.clock.tick() / 1000;
        self.angle += math.pi * self.delta_time;
        self.mouse_pos = list(pygame.mouse.get_pos());

        ############### Player jump
        self.update_jump();
        ############### Keyboard controls
        self.update_movement();
        ############### Reset mouse position
        self.update_mouse();

    def update_jump(self):
        if (30 < self.jump_counter <= 60):
            self.view_matrix.slide(0, self.jump_speed * self.delta_time, 0);
        elif (0 < self.jump_counter < 30):
            self.view_matrix.slide(0, -self.jump_speed * self.delta_time, 0);

        if (self.jump_counter > 0):
            self.jump_counter -= 1;

    def update_movement(self):
        if (self.w_key_pressed):
            if not (self.check_collision('FORWARD')):
                self.view_matrix.slide(0, 0, -self.player_speed * self.delta_time);
            else:
                self.view_matrix.slide(0, 0, (self.player_speed + 1) * self.delta_time);

        elif (self.s_key_pressed):
            if not (self.check_collision('BACKWARD')):
                self.view_matrix.slide(0, 0, self.player_speed * self.delta_time);
            else:
                self.view_matrix.slide(0, 0, (-self.player_speed + 1) * self.delta_time);

        if (self.a_key_pressed):
            if not (self.check_collision('LEFT')):
                self.view_matrix.slide(self.player_speed * self.delta_time, 0, 0);
            else:
                self.view_matrix.slide(-self.player_speed * self.delta_time, 0, 0);

        elif (self.d_key_pressed):
            if not (self.check_collision('RIGHT')):
                self.view_matrix.slide(-self.player_speed * self.delta_time, 0, 0);
            else:
                self.view_matrix.slide(self.player_speed * self.delta_time, 0, 0);

    def update_mouse(self):
        if (self.mouse_pos[0] < 100):
            pygame.mouse.set_pos(screen_size[0] / 2, self.mouse_pos[1]);
            self.mouse_pos[0] = screen_size[0] / 2;
        elif (self.mouse_pos[0] > screen_size[0] - 100):
            pygame.mouse.set_pos(screen_size[0] / 2, self.mouse_pos[1]);
            self.mouse_pos[0] = screen_size[0] / 2;

        if (self.mouse_pos[1] < 100):
            pygame.mouse.set_pos(self.mouse_pos[0], screen_size[1] / 2);
            self.mouse_pos[1] = screen_size[1] / 2;
        elif (self.mouse_pos[1] > screen_size[1] - 100):
            pygame.mouse.set_pos(self.mouse_pos[0], screen_size[1] / 2);
            self.mouse_pos[1] = screen_size[1] / 2;

    def display(self):
        glEnable(GL_DEPTH_TEST);

        glClearColor(0.0, 0.0, 0.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glViewport(0, 0, screen_size[0], screen_size[1]);

        self.projection_matrix.set_perspective(self.field_of_view, screen_size[0] / screen_size[1], 0.5, 100);

        self.shader.set_projection_matrix(self.projection_matrix.get_matrix());
        self.shader.set_view_matrix(self.view_matrix.get_matrix());

        self.shader.set_eye_position(self.view_matrix.eye);

        self.shader.set_light_position(Point(0.0, 10.0, 0.0));
        self.shader.set_light_diffuse(1.0, 1.0, 1.0);
        self.shader.set_light_specular(1.0, 1.0, 1.0);

        self.shader.set_material_specular(1.0, 1.0, 1.0);
        self.shader.set_material_shininess(25);

        self.model_matrix.load_identity();
        self.cube.set_cube_vertices(self.shader);

        self.draw_level();

        pygame.display.flip();

    def draw_level(self):
        self.level_list.pop();

        object_3D = {'color': {'r': 1.0, 'g': 1.0, 'b': 1.0}, 'translation': {'x': 1.0, 'y': 0.0, 'z': 2.0},
                     'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': self.angle}};
        self.level_list.append(object_3D);

        glBindTexture(GL_TEXTURE_2D, self.tex_id01);
        for wall in self.level_list:
            self.draw_cube(wall['color'], wall['translation'], wall['scale'], wall['rotation']);

        glBindTexture(GL_TEXTURE_2D, self.tex_id02);
        floor = {'color': {'r': 1.0, 'g': 0.0, 'b': 0.0}, 'translation': {'x': 10.0, 'y': -3.0, 'z': 27.0},
                 'scale': {'x': 41.0, 'y': 3.0, 'z': 70.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}};

        self.draw_cube(floor['color'], floor['translation'], floor['scale'], floor['rotation']);

        glBindTexture(GL_TEXTURE_2D, self.sprite);
        eye = self.view_matrix.eye;
        view_matrix = self.view_matrix;

        #gun = {'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
        #      'translation': {'x': eye.xPos + math.sin(n.xPos), 'y': eye.yPos - 1.3, 'z': eye.zPos + 1.45},
        #       'scale': {'x': 2.0, 'y': 1.0, 'z': 0.001}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}};

        gun = {'color': {'r': 1.0, 'g': 1.0, 'b': 1.0},
               'translation': {'x': view_matrix.n.xPos, 'y': eye.yPos - 1.3, 'z': eye.zPos + 1.45},
               'scale': {'x': 2.0, 'y': 1.0, 'z': 0.001}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}};

        #self.draw_cube(gun['color'], gun['translation'], gun['scale'], gun['rotation']);

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, self.sprite);
        glEnable(GL_TEXTURE_2D);

        #self.game_display.blit(self.sprite, (screen_size[0] / 2, screen_size[1] / 2));

    def draw_cube(self, color, trans, scale, rotation):
        #self.shader.set_diffuse_texture(self.tex_id);

        self.shader.set_material_diffuse(color['r'], color['g'], color['b']);
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
            self.keyboard_controls(event);

    def keyboard_controls(self, event):
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

            if(event.key == pygame.K_SPACE):
                if(self.jump_counter == 0):
                    self.jump_counter = 60;

            if(event.key == pygame.K_LSHIFT):
                self.sprint_strafe_counter = 100;
                self.player_speed = 20;
                self.player_sprinting = True;

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
                self.sprint_strafe_counter = 0;
                self.player_speed = 10;
                self.player_sprinting = False;

    def check_collision(self, direction):
        eye = self.view_matrix.eye;

        for wall in self.level_list:
            trans = wall['translation'];
            scale = wall['scale'];
            rotation = wall['rotation'];

            if(rotation['y'] == 0.0):
                if(direction == 'FORWARD' or direction == 'BACKWARD'):
                    if(trans['x'] - scale['x'] / 2 <= eye.xPos <= trans['x'] + scale['x'] / 2):
                        if(trans['z'] < eye.zPos):
                            if(trans['z'] - scale['z'] / 2 <= eye.zPos - 2 <= trans['z'] + scale['z'] / 2):
                                return True;
                        elif(trans['z'] > eye.zPos):
                            if(trans['z'] - scale['z'] / 2 <= eye.zPos + 2 <= trans['z'] + scale['z'] / 2):
                                return True;
                        else:
                            return False;

                elif(direction == 'LEFT' or direction == 'RIGHT'):
                    if((trans['z'] - scale['z'] / 2) - 2 <= eye.zPos <= (trans['z'] + scale['z'] / 2) + 2):
                        if(trans['x'] < eye.xPos):
                            if((trans['x'] - scale['x'] / 2) - 2 <= eye.xPos - 4 <= (trans['x'] + scale['x'] / 2) + 2):
                                return True;
                        elif(trans['x'] > eye.xPos):
                            if((trans['x'] - scale['x'] / 2) - 2 <= eye.xPos + 4 <= (trans['x'] + scale['x'] / 2) + 2):
                                return True;
                        else:
                            return False;
            else:
                if(direction == 'FORWARD' or direction == 'BACKWARD'):
                    if(trans['z'] - scale['x'] / 2 <= eye.zPos <= trans['z'] + scale['x'] / 2):
                        if(scale['x'] > scale['z']):
                            if(trans['x'] < eye.xPos):
                                if(trans['x'] - scale['z'] / 2 <= eye.xPos - 2 <= trans['x'] + scale['z'] / 2):
                                    return True;
                            elif(trans['x'] > eye.xPos):
                                if (trans['x'] - scale['z'] / 2 <= eye.xPos + 2 <= trans['x'] + scale['z'] / 2):
                                    return True;
                            else:
                                return False;

                elif (direction == 'LEFT' or direction == 'RIGHT'):
                    if ((trans['x'] - scale['z'] / 2) - 2 <= eye.xPos <= (trans['x'] + scale['z'] / 2) + 2):
                        if (trans['z'] < eye.zPos):
                            if ((trans['z'] - scale['x'] / 2) - 2 <= eye.zPos - 4 <= (trans['z'] + scale['x'] / 2) + 2):
                                return True;
                        elif (trans['z'] > eye.zPos):
                            if ((trans['z'] - scale['x'] / 2) - 2 <= eye.zPos + 4 <= (trans['z'] + scale['x'] / 2) + 2):
                                return True;
                        else:
                            return False;

    def init_game(self):
        pygame.init();
        self.game_display = pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF | pygame.OPENGLBLIT);
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

    def init_level(self):
        self.level_list = [
            {'color': {'r': 1.0, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': 0.0, 'z': -7.0},
             'scale': {'x': 41.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 1.0}, 'translation': {'x': 8.0, 'y': 0.0, 'z': 0.0},
             'scale': {'x': 15.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': math.pi/2, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': -10.0, 'y': 0.0, 'z': 12.0},
             'scale': {'x': 40.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': math.pi/2, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 0.0, 'y': 0.0, 'z': 31.0},
             'scale': {'x': 20.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': 0.0, 'z': 25.0},
             'scale': {'x': 20.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': math.pi/2, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': 30.0, 'y': 0.0, 'z': 25.0},
             'scale': {'x': 80.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': math.pi/2, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 30.0, 'y': 0.0, 'z': 60.0},
             'scale': {'x': 80.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 1.0, 'b': 1.0}, 'translation': {'x': -9.0, 'y': 0.0, 'z': 50.0},
             'scale': {'x': 40.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': math.pi/2, 'z': 0.0}}
        ];

    def load_texture_3D(self, img_path):
        surface = pygame.image.load(sys.path[0] + img_path);
        tex_string = pygame.image.tostring(surface, 'RGBA', 1);
        width = surface.get_width();
        height = surface.get_height();
        tex_id = glGenTextures(1);
        glBindTexture(GL_TEXTURE_2D, tex_id);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string);

        return tex_id;

    def load_texture_2D(self, img_path):
        surface = pygame.image.load(sys.path[0] + img_path).convert_alpha();
        tex_string = pygame.image.tostring(surface, 'RGBA', 1);
        width = surface.get_width();
        height = surface.get_height();
        tex_id = glGenTextures(1);

        glBindTexture(GL_TEXTURE_2D, tex_id);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)

        glBindTexture(GL_TEXTURE_2D, 0);

        return tex_id;


def main():
    game = Game();
    game.game_loop();


if __name__ == '__main__':
    main();