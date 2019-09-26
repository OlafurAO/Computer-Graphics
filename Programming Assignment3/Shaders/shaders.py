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
        '''
        self.position_vec_location      = glGetAttribLocation(self.renderer, 'vec_position');
        self.normal_vector_location     = glGetAttribLocation(self.renderer, 'vec_normal');
        glEnableVertexAttribArray(self.position_vec_location);
        glEnableVertexAttribArray(self.normal_vector_location);

        self.projection_matrix_location = glGetUniformLocation(self.renderer, 'vec_projection_matrix');
        self.model_matrix_location      = glGetUniformLocation(self.renderer, 'vec_model_matrix');
        self.viex_matrix_location       = glGetUniformLocation(self.renderer, 'vec_view_matrix');

        self.color_location = glGetUniformLocation(self.renderer, 'u_color');
        '''

        self.position_vec_location = glGetAttribLocation(self.renderer, 'a_position');
        self.normal_vector_location = glGetAttribLocation(self.renderer, 'a_normal');
        glEnableVertexAttribArray(self.position_vec_location);
        glEnableVertexAttribArray(self.normal_vector_location);

        self.projection_matrix_location = glGetUniformLocation(self.renderer, 'u_projection_matrix');
        self.model_matrix_location = glGetUniformLocation(self.renderer, 'u_model_matrix');
        self.viex_matrix_location = glGetUniformLocation(self.renderer, 'u_view_matrix');

        self.color_location = glGetUniformLocation(self.renderer, 'u_color');


    def render(self):
        glUseProgram(self.renderer);

    def set_model_matrix(self, matrix):
        glUniformMatrix4fv(self.model_matrix_location, 1, True, matrix);

    def set_view_matrix(self, matrix):
        glUniformMatrix4fv(self.viex_matrix_location, 1, True, matrix);

    def set_projection_matrix(self, matrix):
        glUniformMatrix4fv(self.projection_matrix_location, 1, True, matrix);

    def set_solid_color(self, r, g, b):
        glUniform4f(self.color_location, r, g, b, 0.0);

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.position_vec_location, 3, GL_FLOAT, False, 0, vertex_array);

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normal_vector_location, 3, GL_FLOAT, False, 0, vertex_array);