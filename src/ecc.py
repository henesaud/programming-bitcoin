class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime-1}"
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def _are_in_same_field(self, other):
        return self.prime == other.prime

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self._are_in_same_field(other)

    def __add__(self, other):
        if not self._are_in_same_field(other):
            raise TypeError("Cannot add two numbers in different Fields")
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if not self._are_in_same_field(other):
            raise TypeError("Cannot subtract two numbers in different Fields")
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if not self._are_in_same_field(other):
            raise TypeError("Cannot multiply two numbers in different Fields")
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if not self._are_in_same_field(other):
            raise TypeError("Cannot divide two numbers in different Fields")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)


class Point:
    "A point in a elyptcic curve"

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # Accommodates points at infinity. None indicates infinity.
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError(f"({x}, {y}) is not on the curve")

    def _are_in_same_curve(self, other):
        return self.a == other.a and self.b == other.b

    def __eq__(self, other):
        return (
            self.x == other.x and self.y == other.y and self._are_in_same_curve(other)
        )

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if not self._are_in_same_curve(other):
            raise TypeError(f"Points {self}, {other} are not on the same curve")

        if self.x is None:
            return other

        if other.x is None:
            return self

        # Points are additive inverses
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

