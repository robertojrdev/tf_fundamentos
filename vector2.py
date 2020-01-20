
import math

class InvalidOperationException(Exception):
    def __init__(self, op, type1, type2):
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        return "Invalid operation (" + self.op + ") between " + str(self.type1) + " and " + str(self.type2)


class vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __add__(self, v):
        if (isinstance(v, vector2)):
            return vector2(self.x + v.x, self.y + v.y)
        else:
            raise(InvalidOperationException("add", type(self), type(v)))

    def __sub__(self, v):
        if (isinstance(v, vector2)):
            return vector2(self.x - v.x, self.y - v.y)
        else:
            raise(InvalidOperationException("sub", type(self), type(v)))

    def __mul__(self, v):
        if (isinstance(v, (int, float))):
            return vector2(self.x * v, self.y * v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __truediv__(self, v):
        if (isinstance(v, (int, float))):
            return vector2(self.x / v, self.y / v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __eq__(self, v):
        if (isinstance(v, vector2)):
            return (((self - v).magnitude()) < 0.0001)
        else:
            raise(InvalidOperationException("eq", type(self), type(v)))

    def __ne__(self, v):
        if (isinstance(v, vector2)):
            return (((self - v).magnitude()) > 0.0001)
        else:
            raise(InvalidOperationException("neq", type(self), type(v)))

    def __isub__(self, v):
        return self - v

    def __iadd__(self, v):
        return self + v

    def __imul__(self, v):
        return self * v

    def __idiv__(self, v):
        return self / v

    def __neg__(self):
        return vector2(-self.x, -self.y)

    def as_tuple(self):
        return (self.x, self.y)

    def as_int(self):
        return vector2(int(self.x), int(self.y))

    def to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        return self
    