import math
import operator
import types

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __copy__(self):
        return self.__class__(self.x, self.y)

    copy = __copy__

    def __repr__(self):
        return '%.2f,%.2f' % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0 or self.y != 0

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __setitem__(self, key, value):
        l = [self.x, self.y]
        l[key] = value
        self.x, self.y = l

    def __iter__(self):
        return iter((self.x, self.y))

    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y)['xy'.index(c)] for c in name])
        except ValueError:
            raise AttributeError(name)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    __pos__ = __copy__

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    magnitude = __abs__

    def dot(self, other):
        assert isinstance(other, Point)
        return self.x * other.x + self.y * other.y

    def cross(self):
        return Point(self.y, -self.x)

    def angle(self, other):
        """Return the angle to the vector other"""
        return math.acos(self.dot(other) / (self.magnitude()*other.magnitude()))

    def to_point(self, angle, distance, cartesian=False):
        if cartesian:
            return Point(self.x + distance * math.cos(math.radians(angle)), self.y + distance * math.sin(math.radians(angle)))
        else:
            return Point(self.x + distance * math.cos(math.radians(angle)), self.y - distance * math.sin(math.radians(angle)))
