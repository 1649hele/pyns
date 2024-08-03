import builtins as _b


class char:
    def __getattr__(self, item):
        for _t in (str, bytes, int):
            if hasattr(_t, item):
                return getattr(_t(self), item)
        raise AttributeError
    
    def __add__(self, other):
        if isinstance(other, (int, str, bytes, float)):
            return self + char(other)
        elif (isinstance(other, char)):
            return char(self._char + ord(other))
        else:
            raise TypeError
    
    def __sub__(self, other):
        if isinstance(other, (int, str, bytes, float)):
            return self - char(other)
        elif (isinstance(other, char)):
            return char(self._char - ord(other))
        else:
            raise TypeError
    
    def __radd__(self, other):
        return type(other)(self + other)
    
    def __rsub__(self, other):
        if isinstance(other, (int, str, bytes, float)):
            return type(other)(char(other) - self)
        elif (isinstance(other, char)):
            return char(ord(other) - self._char)
        else:
            raise TypeError
    
    def __int__(self):
        return self._char
    
    def __repr__(self):
        return chr(self._char)
    
    def __bytes__(self):
        return self.encode("utf-8")
    
    def __init__(self, __obj):
        if isinstance(__obj, int):
            self._char = __obj
        elif isinstance(__obj, float) and math.isint(__obj):
            self._char = int(__obj)
        elif isinstance(__obj, (str, bytes)) and len(__obj) == 1:
            self._char = ord(__obj)
        elif isinstance(__obj, char):
            self._char = 0 + __obj
        else:
            raise TypeError(
                "__obj must be int or can be int float or char or "
                "len 1 str or len 1 bytes"
            )


def ord(__c):
    if isinstance(__c, char):
        return int(__c)
    return _b.ord(__c)


def chr(__i):
    if isinstance(__i, char):
        return chr(ord(__i))
    return _b.chr(__i)


_g = {}


def globalization(x):
    def new(*args, **kwargs):
        if x.__qualname__ not in _g.keys():
            _g[x.__qualname__] = super(x).__new__(*args, **kwargs)
        return _g[x.__qualname__]
    x.__new__ = new
    return x
