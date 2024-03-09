from src.ecc import FieldElement, Point

P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7


class s256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def __repr__(self):
        return f"{self.num:x}".zfill(64)


class s256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a = s256Field(0)
        b = s256Field(7)

        if isinstance(x, int):
            super().__init__(x=s256Field(x), y=s256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)
