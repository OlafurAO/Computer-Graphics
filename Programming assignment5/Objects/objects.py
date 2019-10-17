from OpenGL.GL import *;
import math;

class Point:
    def __init__(self, xPos, yPos, zPos):
        self.xPos = xPos;
        self.yPos = yPos;
        self.zPos = zPos;

    def __add__(self, other):
        return Point(self.xPos + other.xPos, self.yPos + other.yPos, self.zPos + other.zPos);

    def __sub__(self, other):
        return Vector(self.xPos - other.xPos, self.yPos - other.yPos, self.zPos - other.zPos);


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
                                0.5,  0.5, -0.5]

        self.normal_array = [0.0,  0.0, -1.0,
                             0.0,  0.0, -1.0,
                             0.0,  0.0, -1.0,
                             0.0,  0.0, -1.0,
                             0.0,  0.0,  1.0,
                             0.0,  0.0,  1.0,
                             0.0,  0.0,  1.0,
                             0.0,  0.0,  1.0,
                             0.0, -1.0,  0.0,
                             0.0, -1.0,  0.0,
                             0.0, -1.0,  0.0,
                             0.0, -1.0,  0.0,
                             0.0,  1.0,  0.0,
                             0.0,  1.0,  0.0,
                             0.0,  1.0,  0.0,
                             0.0,  1.0,  0.0,
                            -1.0,  0.0,  0.0,
                            -1.0,  0.0,  0.0,
                            -1.0,  0.0,  0.0,
                            -1.0,  0.0,  0.0,
                             1.0,  0.0,  0.0,
                             1.0,  0.0,  0.0,
                             1.0,  0.0,  0.0,
                             1.0,  0.0,  0.0];

    def set_cube_vertices(self, shader):
        shader.set_position_attribute(self.position_array);
        shader.set_normal_attribute(self.normal_array);

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