try:
    import flat_gui as _f
except ModuleNotFoundError:
    from . import flat_gui as _f
import numpy as _np
try:
    import fm as _math
    from fm import RADIANS, DEGREES, Angle
except ModuleNotFoundError:
    from . import fm as _math
    from .fm import RADIANS, DEGREES, Angle
from typing import Iterable as _Iter


class Sprite:
    def __init__(self, image):
        self.image = _np.array(image, _f.Color, ndmin=3)


class Background:
    def _aor(self, sprites, aor):
        for sprite in sprites:
            if isinstance(sprite, Sprite):
                if aor == "has":
                    if sprite not in self.sprites:
                        return False
                    else:
                        continue
                if aor =="remove" and sprite not in self.sprites:
                    raise ValueError("sprite is not found")
                getattr(self.sprites, aor)(sprite)
            elif isinstance(sprite, _Iter):
                if not self._aor(sprite, aor) and aor == "has":
                    return False
            else:
                raise ValueError("can't %s the %s" % (aor, sprite))
        if aor == "has":
            return True
    
    def add(self, *sprites):
        self._aor(sprites, "append")
    
    def remove(self, *sprites):
        self._aor(sprites, "remove")
    
    def has(self, *sprites):
        return self._aor(sprites, "has")
    
    def getImage(self, angle):
        pass
    
    def __init__(self, *sprites):
        self.sprites = []
        self.add(sprites)
    

X = "x"
Y = "y"
Z = "z"


def part_rotate(axis, angle, x, y, z):
    if isinstance(angle, (tuple, list)):
        angle = Angle(*angle)
    xyz = _math.Quaternion(0, x, y, z)
    angle /= 2
    horn = _math.Quaternion(angle.cos())
    setattr(horn, axis, angle.sin())
    ans = horn * xyz * horn.inverse()
    return (ans.x, ans.y, ans.z)


def word_rotate(axis, angle, x, y, z):
    if isinstance(angle, (tuple, list)):
        angle = Angle(*angle)
    xyz = _math.Quaternion(0, x, y, z)
    angle /= 2
    horn = _math.Quaternion(angle.cos())
    setattr(horn, axis, angle.sin())
    ans = horn.inverse() * xyz * horn
    return (ans.x, ans.y, ans.z)
    

if __name__ == '__main__':
    print(part_rotate(X, (DEGREES, 90), 1, 1, 0))
