import os.path as _path
from os import listdir as _listdir


def split(__obj, *seq, func=lambda self, other: self):
    all = []
    temp = []
    for obj in __obj:
        if obj in seq:
            all.append(func(temp, obj))
            temp = []
        else:
            temp.append(obj)
    all.append(func(temp, type(seq[0])()))
    return all


def flatten(seq):
    res = ()
    for item in seq:
        if isinstance(item, (list, tuple)):
            res += flatten(item)
        elif item is not None:
            res += (item,)
    return res


def to_file(*files):
    files = list(flatten(files))
    i = 0
    while i < len(files):
        if not _path.exists(files[i]):
            files.pop(i)
            continue
        if not _path.isabs(files[i]):
            files[i] = _path.abspath(files[i])
        if _path.isdir(files[i]):
            _dir = files[i][:]
            try:
                files[i] = _listdir(files[i])
            except PermissionError:
                i += 1
                continue
            for j in range(len(files[i])):
                files[i][j] = _path.join(_dir, files[i][j])
            files[i] = to_file(*files[i])
        i += 1
    return flatten(files)


def to_openfiles(*files, way="r"):
    files = list(to_file(*files))
    for i in range(len(files)):
        files[i] = open(files[i], way)
    files = tuple(files)
    return files


def fill(obj, filllens, tofill=None):
    obj.clear()
    if len(filllens) < 1:
        return
    if len(filllens) > 1:
        for _ in range(filllens[0]):
            temp = []
            fill(temp, filllens[1:], tofill)
            obj.append(temp)
    else:
        obj.extend((tofill,) * filllens[0])


class CirculateIter:
    @property
    def len(self):
        return len(self)
    
    def __init__(self, *args):
        self.args = args
        if not self.args:
            raise ValueError("parameter can't to empty")
        self.index = 0
    
    @property
    def args(self):
        return self._args
    
    @args.setter
    def args(self, value):
        if len(value) == 1:
            self.args = value[0]
        else:
            self._args = value
        
    def __iter__(self):
        return iter(self.args)
    
    def next(self):
        temp = _NodeC(self, self.index)
        self.index += 1
        if self.index >= self.len:
            self.index = 0
        return temp
    
    __next__ = next
    
    def __len__(self):
        return len(self.args)
    
    __int__ = __len__


def toTuple(x):
    stack = []
    result = []
    for e in x:
        if e == '(':
            stack.append(result)
            result = []
        elif e == ')':
            t, result = tuple(result), stack.pop()
            result.append(t)
        else:
            result.append(e)
    return tuple(result)
