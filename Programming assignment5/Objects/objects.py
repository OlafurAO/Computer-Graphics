from OpenGL.GL import *;
import math;
import numpy;


class Point:
    def __init__(self, xPos, yPos, zPos):
        self.xPos = xPos;
        self.yPos = yPos;
        self.zPos = zPos;

    def __add__(self, other):
        return Point(self.xPos + other.xPos, self.yPos + other.yPos, self.zPos + other.zPos);

    def __sub__(self, other):
        return Vector(self.xPos - other.xPos, self.yPos - other.yPos, self.zPos - other.zPos);

    def __len__(self):
        return math.sqrt(self.xPos**2 + self.yPos**2 + self.zPos**2);


class Vector:
    def __init__(self, xPos, yPos, zPos):
        self.xPos = xPos;
        self.yPos = yPos;
        self.zPos = zPos;

    def __add__(self, other):
        return Vector(self.xPos + other.xPos, self.yPos + other.yPos, self.zPos + other.zPos);

    def __sub__(self, other):
        return Vector(self.xPos - other.xPos, self.yPos - other.yPos, self.zPos - other.zPos);

    def __mul__(self, multi):
        return Vector(self.xPos * multi, self.yPos * multi, self.zPos * multi);

    def __len__(self):
        return math.sqrt(self.xPos**2 + self.yPos**2 + self.zPos**2);

    def normalize(self):
        len = self.__len__();
        self.xPos /= len;
        self.yPos /= len;
        self.zPos /= len;

    def cross_product(self, other):
        return Vector(self.yPos * other.zPos - self.zPos * other.yPos,
                      self.zPos * other.xPos - self.xPos * other.zPos,
                      self.xPos * other.yPos - self.yPos * other.xPos)

    def dot_product(self, other):
        return self.xPos * other.xPos + self.yPos * other.yPos + self.zPos * other.zPos;


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                               -0.5,  0.5, -0.5,
                                0.5,  0.5, -0.5,
                                0.5, -0.5, -0.5,
                               -0.5, -0.5,  0.5,
                               -0.5,  0.5,  0.5,
                                0.5,  0.5,  0.5,
                                0.5, -0.5,  0.5,
                               -0.5, -0.5, -0.5,
                                0.5, -0.5, -0.5,
                                0.5, -0.5,  0.5,
                               -0.5, -0.5,  0.5,
                               -0.5,  0.5, -0.5,
                                0.5,  0.5, -0.5,
                                0.5,  0.5,  0.5,
                               -0.5,  0.5,  0.5,
                               -0.5, -0.5, -0.5,
                               -0.5, -0.5,  0.5,
                               -0.5,  0.5,  0.5,
                               -0.5,  0.5, -0.5,
                                0.5, -0.5, -0.5,
                                0.5, -0.5,  0.5,
                                0.5,  0.5,  0.5,
                                0.5,  0.5, -0.5];

        self.normal_array = [0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0];

        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0];

    def set_cube_vertices(self, shader):
        shader.set_position_attribute(self.position_array);
        shader.set_normal_attribute(self.normal_array);
        shader.set_uv_attribute(self.uv_array);

    def draw_cube(self):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4);
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4);
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4);
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4);
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4);
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4);


class Sphere:
    def __init__(self, stacks = 12, slices = 24):
        self.vertex_array = [];
        self.slices = slices;

        stack_interval = math.pi / stacks;
        slice_interval = 2.0 * math.pi / slices;
        self.vertex_count = 0;

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval;

            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval;

                self.vertex_array.append(math.sin(stack_angle) * math.cos(slice_angle));
                self.vertex_array.append(math.cos(stack_angle));
                self.vertex_array.append(math.sin(stack_angle) * math.sin(slice_angle));

                self.vertex_array.append(math.sin(stack_angle + stack_interval) * math.cos(slice_angle));
                self.vertex_array.append(math.cos(stack_angle + stack_interval));
                self.vertex_array.append(math.sin(stack_angle + stack_interval) * math.sin(slice_angle));

                self.vertex_count += 2;

    def set_vertices(self, shader):
        shader.set_position_attribute(self.vertex_array);
        shader.set_normal_attribute(self.vertex_array);

    def draw_sphere(self, shader):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2);


class Material:
    def __init__(self, diffuse = None, specular = None, shininess = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess


class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict()
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()

    def add_vertex(self, mesh_id, position, normal, uv=None):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.xPos, position.yPos, position.zPos,
                                        normal.xPos, normal.yPos, normal.zPos]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat

    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id],
                                                      dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]

            shader.set_material_diffuse(material.diffuse)
            shader.set_material_specular(material.specular)
            shader.set_material_shininess(material.shininess)
            shader.set_attribute_buffers(self.vertex_buffer_ids[mesh_id])
            #shader.set_attribute_buffers_with_uv(self.vertex_buffer_ids[mesh_id])

            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)
