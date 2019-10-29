from OpenGL.GL import *;
from OpenGL.GLU import *
import pygame;
import math;
import sys;

from Shaders.shaders import *;
from Matrix.matrix import *;
from Objects.gun import *;
from Objects.enemy import *;
import obj_3D_loading;

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

        eye = self.view_matrix.eye;

        gun_model = obj_3D_loading.load_obj_file(sys.path[0] +
                                                '/Assets/Art/models', 'shotgunShort.obj');
        bullet_model = obj_3D_loading.load_obj_file(sys.path[0] +
                                                '/Assets/Art/models', 'ammo_pistol.obj');

        self.player_gun = Gun(gun_model, bullet_model, self.view_matrix, eye.xPos, eye.yPos, eye.zPos);
        self.bullet_list = [];

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

        #self.sprite = self.load_texture_2D('/Assets/Art/Spritesheets/Player/tile000.png');
        self.gun_sprite = self.load_texture_2D('/Assets/Art/gun.jpg');
        self.enemy_sprite = self.load_texture_2D('/Assets/Art/doom_imp.jpg');

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

        for bullet in self.bullet_list:
            bullet.update_movement(self.delta_time);

            if(bullet.wall_collision_check(self.level_list) or bullet.enemy_collision_check(self.enemy_list)):
                self.bullet_list.remove(bullet);

        for enemy in self.enemy_list:
            if(enemy.is_dead()):
                self.enemy_list.remove(enemy);

            enemy.set_translation(self.view_matrix);
            enemy.set_rotation(self.view_matrix);

    def update_jump(self):
        if (30 < self.jump_counter <= 60):
            self.view_matrix.slide(0, self.jump_speed * self.delta_time, 0);
        elif (0 < self.jump_counter < 30):
            self.view_matrix.slide(0, -self.jump_speed * self.delta_time, 0);

        if (self.jump_counter > 0):
            self.jump_counter -= 1;
            eye = self.view_matrix.eye;
            self.player_gun.set_translation(self.view_matrix);

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
                self.view_matrix.slide(0, 0, -(self.player_speed + 1) * self.delta_time);

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

        self.player_gun.set_translation(self.view_matrix)
        #self.player_gun.set_translation(self.view_matrix, 0, 0, 0);

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
        self.shader.set_light_diffuse(Color(1.0, 1.0, 1.0));
        self.shader.set_light_specular(Color(1.0, 1.0, 1.0));

        self.shader.set_material_specular(Color(1.0, 1.0, 1.0));
        self.shader.set_material_shininess(25);

        self.model_matrix.load_identity();
        self.cube.set_cube_vertices(self.shader);

        self.draw_level();

        pygame.display.flip();

    def draw_level(self):
        glBindTexture(GL_TEXTURE_2D, self.tex_id01);
        for wall in self.level_list:
            self.draw_cube(wall['color'], wall['translation'], wall['scale'], wall['rotation']);
        #glBindTexture(GL_TEXTURE_2D, self.tex_id02);
        floor = {'color': {'r': 1.0, 'g': 1.0, 'b': 1.0}, 'translation': {'x': 10.0, 'y': -3.0, 'z': 27.0},
                 'scale': {'x': 41.0, 'y': 3.0, 'z': 70.0}, 'rotation': {'x': 0.0, 'y': 0.0, 'z': 0.0}};
        self.draw_cube(floor['color'], floor['translation'], floor['scale'], floor['rotation']);

        #glDeleteTextures(self.tex_id02)
        #glBindTexture(GL_TEXTURE_2D, self.gun_sprite);
        gun_trans = self.player_gun.get_transformations();
        gun_model = self.player_gun.get_model();

        self.draw_model(gun_model, gun_trans['color'], gun_trans['translation'],
                        gun_trans['scale'], gun_trans['rotation']);

        for i in self.bullet_list:
            bullet = i.get_transformations();
            model = i.get_model();
            self.draw_model(model, bullet['color'], bullet['translation'], bullet['scale'], bullet['rotation']);

        glBindTexture(GL_TEXTURE_2D, self.enemy_sprite);
        glDeleteTextures(self.enemy_sprite)
        for i in self.enemy_list:
            enemy = i.get_transformations();
            self.draw_cube(enemy['color'], enemy['translation'], enemy['scale'], enemy['rotation']);

    def draw_cube(self, color, trans, scale, rotation):
        self.shader.set_material_diffuse(Color(color['r'], color['g'], color['b']));
        self.model_matrix.push_matrix();

        self.model_matrix.add_translation(trans['x'], trans['y'], trans['z']);

        self.model_matrix.add_rotation_x(rotation['x']);
        self.model_matrix.add_rotation_y(rotation['y']);
        self.model_matrix.add_rotation_z(rotation['z']);

        self.model_matrix.add_scaling(scale['x'], scale['y'], scale['z']);

        self.shader.set_model_matrix(self.model_matrix.get_model_matrix());
        self.cube.draw_cube();
        self.model_matrix.pop_matrix();

    def draw_model(self, model, color, trans, scale, rotation):
        self.shader.set_material_diffuse(Color(color['r'], color['g'], color['b']));
        self.model_matrix.push_matrix();

        self.model_matrix.add_translation(trans['x'], trans['y'], trans['z']);

        self.model_matrix.add_rotation_x(rotation['x']);
        self.model_matrix.add_rotation_y(rotation['y']);
        self.model_matrix.add_rotation_z(rotation['z']);

        self.model_matrix.add_scaling(scale['x'], scale['y'], scale['z']);

        self.shader.set_model_matrix(self.model_matrix.get_model_matrix());
        model.draw(self.shader)
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
                self.player_gun.set_rotation(self.delta_time * mouse_x_pos_movement);

            elif(new_mouse_pos[0] < self.mouse_pos[0]):
                mouse_x_pos_movement = self.mouse_pos[0] - new_mouse_pos[0];
                self.view_matrix.yaw(-self.delta_time * mouse_x_pos_movement);
                self.mouse_pos = list(new_mouse_pos);
                self.player_gun.set_rotation(-self.delta_time * mouse_x_pos_movement);

        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(pygame.mouse.get_pressed()[0]):
                bullet = self.player_gun.fire_gun(self.view_matrix);
                self.bullet_list.append(bullet);


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
        if(direction == 'FORWARD'):
            self.view_matrix.slide(0, 0, -10 * self.delta_time);
        elif(direction == 'BACKWARD'):
            self.view_matrix.slide(0, 0, 10 * self.delta_time);
        elif(direction == 'LEFT'):
            self.view_matrix.slide(10 * self.delta_time, 0, 0);
        elif(direction == 'RIGHT'):
            self.view_matrix.slide(-10 * self.delta_time, 0, 0);

        eye = self.view_matrix.eye;

        for wall in self.level_list:
            trans = wall['translation'];
            scale = wall['scale'];
            rotation = wall['rotation'];

            if(rotation['y'] == 0.0):
                if(direction == 'FORWARD' or direction == 'BACKWARD'):
                    if(trans['x'] - scale['x'] / 2 < eye.xPos < trans['x'] + scale['x'] / 2):
                        if(trans['z'] < eye.zPos):
                            if(trans['z'] - scale['z'] / 2 < eye.zPos - 2 < trans['z'] + scale['z'] / 2):
                                return True;
                        elif(trans['z'] > eye.zPos):
                            if(trans['z'] - scale['z'] / 2 < eye.zPos + 2 < trans['z'] + scale['z'] / 2):
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

        self.enemy_list = [
            #Enemy((1.0, 1.0, 1.0), (1.0, 0.0, 5.0), (0.001, 3.0, 3.0), (0.0, 0.0, 0.0)),
            Enemy((1.0, 1.0, 1.0), (20.0, 0.0, 20.0), (3.0, 3.0, 3.0), (0.0, 0.0, 0.0)),
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