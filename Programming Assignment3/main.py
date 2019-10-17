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
        self.init_gamepad();

        self.mouse_sensitivity = 5;
        self.angle = 0;

        self.player_speed = 10;
        self.jump_speed = 10;
        self.sprint_strafe_counter = 0;
        self.sprint_strafe_speed = 5;
        self.jump_counter = 0;

        self.game_over = False;
        self.player_sprinting = False;

    def update(self):
        self.delta_time = self.clock.tick() / 1000;
        self.angle += math.pi * self.delta_time;
        self.mouse_pos = list(pygame.mouse.get_pos());

        ############### Player sprint strafe
        self.update_sprint();
        ############### Player jump
        self.update_jump();
        ############### Keyboard controls
        self.update_movement();
        ############### Reset mouse position
        self.update_mouse();

    def update_sprint(self):
        if (50 < self.sprint_strafe_counter <= 100):
            self.view_matrix.slide(self.sprint_strafe_speed * self.delta_time, 0, 0);

            if (self.sprint_strafe_counter >= 75):
                self.view_matrix.slide(0, self.sprint_strafe_speed * self.delta_time, 0);
            else:
                self.view_matrix.slide(0, -self.sprint_strafe_speed * self.delta_time, 0);

        elif (0 < self.sprint_strafe_counter < 50):
            self.view_matrix.slide(-self.sprint_strafe_speed * self.delta_time, 0, 0);

            if (self.sprint_strafe_counter >= 26):
                self.view_matrix.slide(0, self.sprint_strafe_speed * self.delta_time, 0);
            else:
                self.view_matrix.slide(0, -self.sprint_strafe_speed * self.delta_time, 0);

        if (self.sprint_strafe_counter > 0):
            self.sprint_strafe_counter -= 1;
        elif (self.sprint_strafe_counter == 0 and self.player_sprinting):
            self.sprint_strafe_counter = 100;

        if(self.jump_counter == 0):
            if(self.view_matrix.eye.yPos > 0.5):
                self.view_matrix.eye.yPos = 0;
            elif(self.view_matrix.eye.yPos < -0.6):
                self.view_matrix.eye.yPos = 0;

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

        elif (self.s_key_pressed):
            if not (self.check_collision('BACKWARD')):
                self.view_matrix.slide(0, 0, self.player_speed * self.delta_time);

        if (self.a_key_pressed):
            if not (self.check_collision('LEFT')):
                self.view_matrix.slide(self.player_speed * self.delta_time, 0, 0);
        elif (self.d_key_pressed):
            if not (self.check_collision('RIGHT')):
                self.view_matrix.slide(-self.player_speed * self.delta_time, 0, 0);

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
        #glDisable(GL_DEPTH_TEST);
        glClearColor(0.0, 0.0, 0.0, 1.0);
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
        for wall in self.level_list:
            self.draw_cube(wall['color'], wall['translation'], wall['scale'], wall['rotation']);

        floor = {'color': {'r': 1.0, 'g': 0.0, 'b': 0.0}, 'translation': {'x': 10.0, 'y': -3.0, 'z': 27.0},
                 'scale': {'x': 41.0, 'y': 3.0, 'z': 70.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}}

        self.draw_cube(floor['color'], floor['translation'], floor['scale'], floor['rotation']);

        # Rotating 3D objects
        object_3D = {'color': {'r': 0.2, 'g': 0.2, 'b': 0.5}, 'translation': {'x': 5.0, 'y': 0.0, 'z': 5.0},
             'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': self.angle}};

        self.draw_cube(object_3D['color'], object_3D['translation'], object_3D['scale'], object_3D['rotation']);
        self.object_list.append(object_3D);

        object_3D = {'color': {'r': 1.0, 'g': 0.0, 'b': 0.0}, 'translation': {'x': 5.0, 'y': 0.0, 'z': 0.0},
                     'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': self.angle, 'z': 0.0}};

        self.draw_cube(object_3D['color'], object_3D['translation'], object_3D['scale'], object_3D['rotation']);
        self.object_list.append(object_3D);

        object_3D = {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': 5.0, 'y': 0.0, 'z': -5.0},
                     'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}, 'rotation': {'x': self.angle, 'y': self.angle, 'z': 0.0}};

        self.draw_cube(object_3D['color'], object_3D['translation'], object_3D['scale'], object_3D['rotation']);
        self.object_list.append(object_3D);

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
            self.keyboard_controls(event);
            #if(len(self.gamepad_list) > 0):
                #self.gamepad_controls(event);

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

            '''
            if(new_mouse_pos[1] > self.mouse_pos[1]):
                mouse_y_pos_movement = self.mouse_pos[1] - new_mouse_pos[1];
                self.view_matrix.pitch(self.delta_time * mouse_y_pos_movement);
                self.mouse_pos = list(new_mouse_pos);
            elif(new_mouse_pos[1] < self.mouse_pos[1]):
                mouse_y_pos_movement = new_mouse_pos[1] - self.mouse_pos[1];
                self.view_matrix.pitch(-self.delta_time * mouse_y_pos_movement);
                self.mouse_pos = list(new_mouse_pos);
            '''

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

    def gamepad_controls(self, event):
        if(event.type == pygame.JOYAXISMOTION):
            axis = self.gamepad_list[event.joy].get_axis(event.axis);

            if(axis < -1.0):
                return;

            # Left analog stick
            if(event.axis == 0):
                if(-1.0  <= axis <= -0.5):
                    self.a_key_pressed = True;
                elif(0.5 <= axis <= 1.0):
                    self.d_key_pressed = True;
                else:
                    self.a_key_pressed = False;
                    self.d_key_pressed = False;

            elif(event.axis == 1):
                if(-1.0 <= axis <= -0.5):
                    self.w_key_pressed = True;
                elif(0.5 <= axis <= 1.0):
                    self.s_key_pressed = True;
                else:
                    self.s_key_pressed = False;
                    self.w_key_pressed = False;

            # Right analog stick
            elif(event.axis == 2):
                if(-1.0 <= axis <= -0.4):
                    self.view_matrix.yaw(-self.delta_time * 5);
                elif(0.4 <= axis <= 1.0):
                    self.view_matrix.yaw(self.delta_time * 5);

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
                    if(trans['z'] - scale['z'] / 2 <= eye.zPos  <= trans['z'] + scale['z'] / 2):
                        if(trans['x'] < eye.xPos):
                            if(trans['x'] - scale['x'] / 2 <= eye.xPos - 4 <= trans['x'] + scale['x'] / 2):
                                return True;
                        elif(trans['x'] > eye.xPos):
                            if(trans['x'] - scale['x'] / 2 <= eye.xPos + 4 <= trans['x'] + scale['x'] / 2):
                                return True;
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

                elif (direction == 'LEFT' or direction == 'RIGHT'):
                    pass


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

    def init_level(self):
        self.object_list = [];
        '''
        self.level_list = [
            {'color': {'r': 1.0, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': 0.0, 'z': -7.0},
             'scale': {'x': 41.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': -10.0, 'y': 0.0, 'z': 12.0},
             'scale': {'x': 40.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}}
        '''

        self.level_list = [
            {'color': {'r': 1.0, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': 0.0, 'z': -7.0},
             'scale': {'x': 41.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 1.0}, 'translation': {'x': 8.0, 'y': 0.0, 'z': 0.0},
             'scale': {'x': 15.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': 3.8, 'y': 0.0, 'z': 8.0},
             'scale': {'x': 10.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': -10.0, 'y': 0.0, 'z': 12.0},
             'scale': {'x': 40.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': -1.0, 'y': 0.0, 'z': 15.0},
             'scale': {'x': 15.0, 'y': 5.0, 'z': 2.5}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 0.0, 'y': 0.0, 'z': 31.0},
             'scale': {'x': 20.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': 0.0, 'z': 25.0},
             'scale': {'x': 20.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 1.0, 'b': 0.0}, 'translation': {'x': 30.0, 'y': 0.0, 'z': 25.0},
             'scale': {'x': 80.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}},

            {'color': {'r': 0.0, 'g': 0.0, 'b': 1.0}, 'translation': {'x': 30.0, 'y': 0.0, 'z': 60.0},
             'scale': {'x': 80.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}},

            {'color': {'r': 0.5, 'g': 1.0, 'b': 1.0}, 'translation': {'x': -9.0, 'y': 0.0, 'z': 50.0},
             'scale': {'x': 40.0, 'y': 5.0, 'z': 1.0}, 'rotation': {'x': 0.0, 'y': 4.713, 'z': 0.0}}
        ];

    def init_gamepad(self):
        self.gamepad_list = [];

        for gamepad in range(pygame.joystick.get_count()):
            self.gamepad_list.append(pygame.joystick.Joystick(gamepad));

        for gamepad in self.gamepad_list:
            gamepad.init();


def main():
    game = Game();
    game.game_loop();


if __name__ == '__main__':
    main();