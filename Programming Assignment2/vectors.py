class Vector:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y);

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other);

    def get_dot_product(self, other):
        return self.x * other.x + self.y * other.y


class Point:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y);