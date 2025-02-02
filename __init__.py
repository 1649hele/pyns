import builtins as _b
import sys as _s
import os as _o
import typing as _t
import _io
try:
    import structures, fm, func, flat_gui, sound, file, screen, url, win, stereoscopic_gui, iter, module
except ImportError:
    from . import structures, fm, func, flat_gui, sound, file, screen, url, win, stereoscopic_gui, iter, module


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


SPACE = ("\n", " ", "\t", "\0")
EOF = "\0"
INT_MIN = - (1 << 31)
INT_MAX = -1 - INT_MIN
LLONG_MIN = - (1 << 63)
LLONG_MAX = -1 - LLONG_MIN


def getchar(file, size=1):
    temp = file.read(size)
    return EOF if temp == "" else temp


class PyIstream:
    def __init__(self, *args, **kwargs):
        self.set_file(*args, **kwargs)
    
    def set_file(self, file, *args, **kwargs):
        if isinstance(file, (str, bytes, _o.PathLike)):
            self.filename = file
            self.file = open(file, "r", *args, **kwargs)
        elif hasattr(file, "read"):
            self.filename = file
            self.file = file
        else:
            raise TypeError("expected str, bytes, os.PathLike or IO, not %s" % type(file))
        self.cache = ""
    
    def get(self, *end, size=-1):
        end = iter.flatten(end)
        if not (end or size):
            end = SPACE
        if len(end) == 1 and size == 0 and isinstance(end[0], int):
            size = end[0]
            end = ()
        
        if self.file is None:
            raise NotImplementedError("self parameter must be activated")
        
        cnt = 0
        while cnt < size:
            c = getchar(self.file)
            if c in end:
                break
            self.cache += c
            cnt += 1
        
        temp = self.cache.strip()
        self.cache = ""
        return temp
    
    def close(self):
        try:
            with self.file:
                pass
        except:
            pass
        self.file = None
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __repr__(self):
        return "PyIstream object at %s" % self.filename
    
    __call__ = get
    
    def __rshift__(self, other):
        return self.get(other)
    
    __lshift__ = __rshift__


pycin = PyIstream(_s.stdin) # Unable to debug


def freopen(file, stream):
    stream.set_file(file)


_g = {}


def globalization(x, g=_g):
    _new = x.__new__
    
    def new(*args, **kwargs):
        if x.__qualname__ not in g.keys():
            g[x.__qualname__] = _new(*args, **kwargs)
        return g[x.__qualname__]
    
    x.__new__ = new
    return x
