import math;
from Objects.objects import *;

class Model_Matrix:
    def __init__(self):
        self.model_matrix = [1, 0, 0, 0,
                             0, 1, 0, 0,
                             0, 0, 1, 0,
                             0, 0, 0, 1];
        self.model_matrix_list = [];

    def load_identity(self):
        self.model_matrix = [1, 0, 0, 0,
                             0, 1, 0, 0,
                             0, 0, 1, 0,
                             0, 0, 0, 1];

    def copy_matrix(self):
        new_matrix = [0] * 16;
        for i in range(16):
            new_matrix[i] = self.model_matrix[i];
        return new_matrix;

    def apply_transformation(self, transformation_matrix):
        count = 0;
        new_matrix = [0] * 16;
        for row in range(4):
            for col in range(4):
                for index in range(4):
                    new_matrix[count] += self.model_matrix[row * 4 + index] * transformation_matrix[col + 4 * index];
                count += 1;

        self.model_matrix = new_matrix;

    def add_nothing(self):
        new_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1];

        self.apply_transformation(new_matrix);

    def add_translation(self, x, y, z):
        new_matrix = [1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1];

        self.apply_transformation(new_matrix);

    def add_rotation_x(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        new_matrix = [1, 0,  0, 0,
                        0, c, -s, 0,
                        0, s,  c, 0,
                        0, 0,  0, 1];

        self.apply_transformation(new_matrix);

    def add_rotation_y(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        new_matrix = [c, 0, s, 0,
                        0, 1, 0, 0,
                       -s, 0, c, 0,
                        0, 0, 0, 1];

        self.apply_transformation(new_matrix);

    def add_rotation_z(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        new_matrix = [c, -s, 0, 0,
                        s,  c, 0, 0,
                        0,  0, 1, 0,
                        0,  0, 0, 1];

        self.apply_transformation(new_matrix);

    def add_scaling(self, x, y, z):
        new_matrix = [x, 0, 0, 0,
                        0, y, 0, 0,
                        0, 0, z, 0,
                        0, 0, 0, 1];

        self.apply_transformation(new_matrix);

    def push_matrix(self):
        self.model_matrix_list.append(self.copy_matrix());

    def pop_matrix(self):
        self.model_matrix = self.model_matrix_list.pop();

    def get_model_matrix(self):
        return self.model_matrix;

class View_Matrix:
    def __init__(self):
        self.eye = Point(0, 0, 0);
        self.u = Vector(1, 0, 0);
        self.v = Vector(0, 1, 0);
        self.n = Vector(0, 0, 1);

    def view(self, eye, center, up):
        self.eye = eye;
        self.n = (eye - center);
        self.n.normalize();
        self.u = up.cross_product(self.n);
        self.u.normalize();
        self.v = self.n.cross_product(self.u);

    def slide(self, del_u, del_v, del_n):
        self.eye += self.u * del_u + self.v * del_v + self.n * del_n;

    def roll(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        tmp_u = self.u * c + self.v * s;
        self.v = self.u * -s + self.v * c;
        self.u = tmp_u;

    def pitch(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        tmp_v = self.v * c + self.n * s;
        self.n = self.v * -s + self.n * c;
        self.v = tmp_v;

    def yaw(self, angle):
        c = math.cos(angle);
        s = math.sin(angle);

        tmp_n = self.n * c + self.u * s;
        self.u = self.n * -s + self.u * c;
        self.n = tmp_n;

    def get_matrix(self):
        minus_eye = Vector(-self.eye.xPos, -self.eye.yPos, -self.eye.zPos);
        return [self.u.xPos, self.u.yPos, self.u.zPos, minus_eye.dot_product(self.u),
                self.v.xPos, self.v.yPos, self.v.zPos, minus_eye.dot_product(self.v),
                self.n.xPos, self.n.yPos, self.n.zPos, minus_eye.dot_product(self.n),
                     0     ,      0     ,      0     ,     1];

class Projection_Matrix:
    def __init__(self):
        self.left       = -1;
        self.right      =  1;
        self.bottom     = -1;
        self.top        =  1;
        self.near       = -1;
        self.far        =  1;

        self.is_orthographic = True;

    def set_perspective(self, field_of_view, aspect_ratio, near, far):
        self.near = near;
        self.far = far;

        self.top = near * math.tan(field_of_view / 2);
        self.bottom = -self.top;
        self.right = self.top - aspect_ratio;
        self.left = -self.right;

        self.is_orthographic = False;

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left;
        self.right = right;
        self.bottom = bottom;
        self.top = top;

        self.near = near;
        self.far = far;

        self.is_orthographic = True;

    def get_matrix(self):
        if(self.is_orthographic):
            a = 2 / (self.right - self.left);
            b = -(self.right + self.left) / (self.right - self.left);
            c = 2 / (self.top - self.bottom);
            d = -(self.top + self.bottom) / (self.top - self.bottom);
            e = 2 / (self.near - self.far);
            f = (self.near + self.far) / (self.near - self.far);

            return [a,  0,  0,  b,
                    0,  c,  0,  d,
                    0,  0,  e,  f,
                    0,  0,  0,  1];
        else:
            a = (2 * self.near) / (self.right - self.left);
            b = (self.right + self.left) / (self.right - self.left);
            c = (2 * self.near) / (self.top - self.bottom);
            d = (self.top + self.bottom) / (self.top - self.bottom);
            e = -(self.far + self.near) / (self.far - self.near);
            f = -(2 * self.far + self.near) / (self.far - self.near);

            return [a,  0,  b,  0,
                    0,  c,  d,  0,
                    0,  0,  e,  f,
                    0,  0, -1,  0];