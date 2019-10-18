from OpenGL.GL import *;
import math;
import sys;

class Shader3D:
    def __init__(self):
        self.renderer = glCreateProgram();
        self.init_shader();
        self.init_vec_locations();

    def init_shader(self):
        vertex_shader = glCreateShader(GL_VERTEX_SHADER);
        vertex_shader_file = open(sys.path[0] + '/Shaders/3Dshader.vert');
        frag_shader = glCreateShader(GL_FRAGMENT_SHADER);
        frag_shader_file = open(sys.path[0] + '/Shaders/3Dshader.frag');

        glShaderSource(vertex_shader, vertex_shader_file.read());
        glCompileShader(vertex_shader);
        glShaderSource(frag_shader, frag_shader_file.read());
        glCompileShader(frag_shader);

        vertex_shader_file.close();
        frag_shader_file.close();

        vertex_result = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS);
        frag_result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS);

        if(vertex_result != 1):
            print(str(glGetShaderInfoLog(vertex_shader)));
        if(frag_result != 1):
            print(str(glGetShaderInfoLog(frag_shader)));

        glAttachShader(self.renderer, vertex_shader);
        glAttachShader(self.renderer, frag_shader);
        glLinkProgram(self.renderer);

    def init_vec_locations(self):
        self.position_vec_location              = glGetAttribLocation(self.renderer, 'a_position');
        self.normal_vector_location             = glGetAttribLocation(self.renderer, 'a_normal');
        self.uv_location                        = glGetAttribLocation(self.renderer, 'a_uv');
        glEnableVertexAttribArray(self.position_vec_location);
        glEnableVertexAttribArray(self.normal_vector_location);
        glEnableVertexAttribArray(self.uv_location);

        self.projection_matrix_location         = glGetUniformLocation(self.renderer, 'u_projection_matrix');
        self.model_matrix_location              = glGetUniformLocation(self.renderer, 'u_model_matrix');
        self.viex_matrix_location               = glGetUniformLocation(self.renderer, 'u_view_matrix');

        self.eye_pos_location                   = glGetUniformLocation(self.renderer, 'u_eye_position')

        self.light_pos_location                 = glGetUniformLocation(self.renderer, 'u_light_position');
        self.light_diffuse_location             = glGetUniformLocation(self.renderer, 'u_light_diffuse');
        self.light_specular_location            = glGetUniformLocation(self.renderer, 'u_light_specular');

        self.material_diffuse_location          = glGetUniformLocation(self.renderer, 'u_material_diffuse');
        self.material_specular_location         = glGetUniformLocation(self.renderer, 'u_material_specular');
        self.material_shininess_location        = glGetUniformLocation(self.renderer, 'u_material_shininess');

        self.diffuse_texture_location        = glGetUniformLocation(self.renderer, 'u_tex01');

    def render(self):
        glUseProgram(self.renderer);

    def set_model_matrix(self, matrix):
        glUniformMatrix4fv(self.model_matrix_location, 1, True, matrix);

    def set_view_matrix(self, matrix):
        glUniformMatrix4fv(self.viex_matrix_location, 1, True, matrix);

    def set_projection_matrix(self, matrix):
        glUniformMatrix4fv(self.projection_matrix_location, 1, True, matrix);

    def set_eye_position(self, pos):
        glUniform4f(self.eye_pos_location, pos.xPos, pos.yPos, pos.zPos, 1.0);

    def set_light_position(self, pos):
        glUniform4f(self.light_pos_location, pos.xPos, pos.yPos, pos.zPos, 1.0);

    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.light_diffuse_location, r, g, b, 1.0);

    def set_light_specular(self, r, g, b):
        glUniform4f(self.light_specular_location, r, g, b, 1.0);

    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.material_diffuse_location, r, g, b, 1.0);

    def set_material_specular(self, r, g, b):
        glUniform4f(self.material_specular_location, r, g, b, 1.0);

    def set_material_shininess(self, shininess):
        glUniform1f(self.material_shininess_location, shininess);

    def set_diffuse_texture(self, texture):
        glUniform1f(self.diffuse_texture_location, texture);

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.position_vec_location, 3, GL_FLOAT, False, 0, vertex_array);

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normal_vector_location, 3, GL_FLOAT, False, 0, vertex_array);

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uv_location, 2, GL_FLOAT, False, 0, vertex_array);