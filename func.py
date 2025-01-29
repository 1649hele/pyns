import functools
import inspect as _i
import os as _o
import sys as _s
import threading as _t
import time as _d
import traceback as _r
from collections import defaultdict as _defaultdict
from typing import Callable


_stdout = _s.stdout


def set_function(module, name, newname=None):
    if newname is None:
        newname = name
    temp = getattr(module, name)
    exec("%s = temp" % newname)


class Thread(_t.Thread):
    def __init__(self, target, *args, group=None, **kwargs):
        self.event = _t.Event
        
        def g():
            if self.event.is_set():
                pass
        super().__init__(group, target, *args, **kwargs)
    
    def stop(self):
        self.event.set()


def flash_print(
    *values,
    sep=" ",
    file=None,
    delay=0,
    end="\n",
    new_thread=True,
    _raise=True,
):
    delay /= 1000
    
    if file is None:
        file = _s.stdout
    
    def prints():
        for value in values:
            for _char in value:
                char = str(_char)
                if char == "\000":
                    break
                elif char == "\b" and file != _stdout:
                    readLen = open(file.name).read()
                    readLen = len(readLen)
                    if readLen > 0:
                        file.truncate(readLen - 1)
                    elif _raise:
                        raise ValueError("file is be None can't remove char")
                else:
                    print(char, end="", flush=True, file=file)
                _ordChar = ord(char)
                if char not in ("\n", "\r", "", "\t", "\f", "\a", "\b") and (
                    (
                        32 <= _ordChar <= 127 or
                        1469 >= _ordChar >= 3278
                    ) and _ordChar not in (3252, 3258, 3259)
                ):
                    _d.sleep(delay)
            print(sep, end="", file=file)
        print(end, end="", file=file)
    if new_thread:
        _t.Thread(target=prints).start()
    else:
        prints()


class Count:
    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, value):
        self._number = value
    
    def __init__(self, x, func=lambda self: self + 1):
        self._number = x
        self._func = lambda: None
        self.func = func
    
    def __iter__(self):
        return self
    
    def __next__(self):
        temp = self._number
        self._number = self.func(self._number)
        return temp
    
    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self, value):
        if isinstance(value, str):
            self._func = getattr(
                type(self._number),
                value,
                None,
            )
            if self._func is None:
                self._func = getattr(self._number, "__%s__" % value)
        elif isinstance(value, Callable):
            self._func = value
        else:
            raise ValueError(
                "value parameter be str or Callable, not %s" % type(value).__name__)
    
    @func.deleter
    def func(self):
        raise AttributeError("func atrribute can't delete")
        

class InitError(Exception):
    pass


class CallWrapper:
    def __init__(self, *funcs, newThread=False, raised=False, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        self._func = None
        self._inited = False
        if len(funcs) > 1:
            self.func = overload_dummy(*funcs)
        else:
            self.func = funcs[0]
        self.args   = args
        self.kwargs = kwargs
        self.newThread = newThread
        self.raised = raised
    
    @property
    def func(self):
        if not self._inited:
            raise InitError("Object not initialized")
        return self._func
    
    @func.setter
    def func(self, value):
        if not isinstance(value, Callable):
            raise ValueError("value parameter is not a Callable")
        self._inited = True
        self._func = value
        self.__name__ = value.__name__
        self.__code__ = value.__code__
        self.__qualname__ = value.__qualname__
        self.__module__ = value.__module__
        self.code = value.__code__
    
    @func.deleter
    def func(self):
        self._func = None
        self.__name__ = None
        self.__code__ = None
        self.code = None
        self.inited = False
    
    def start(self, *args, **kwargs):
        if not self._inited:
            if self.raised:
                raise InitError("Object not initialized")
            else:
                return
        if not (args or kwargs):
            args, kwargs = self.args, self.kwargs
        try:
            if self.newThread:
                self.thread = Thread(
                    None,
                    self.func,
                    self.__name__,
                    args,
                    kwargs,
                    daemon=True,
                )
                self.thread.start()
            else:
                return self.func(*args, **kwargs)
        except SystemExit:
            raise
        except:
            print("func.py in CallWrapper.start", file=_s.stderr)
            lines = _r.format_exc().split("\n")
            r = lines[-2]
            new = lines[0]
            new = [new]
            _lines = lines[3:-2]
            _lines[0] = _lines[0].lstrip().lstrip("^")
            lines = new + _lines
            for line in lines:
                if not line:
                    lines.remove(line)
            lines = "\n  ".join(lines)
            lines = "  " + lines
            lines += "\n"
            lines += r
            print(lines, file=_s.stderr)
            if self.raised:
                exit(1)
    
    __call__ = start


class Thread(_t.Thread):
    def __init__(self, func, *, args=(), addself=0, **kwargs):
        self.event = _t.Event()
        if addself is not False:
            args = list(args)
            args.insert(addself, self)
            args = tuple(args)
        if "name" not in kwargs:
            kwargs["name"] = func.__name__
        super(Thread, self).__init__(target=func, args=args, **kwargs)
    
    def stop(self):
        self.event.set()
    
    def is_stop(self):
        return self.event.is_set()

        
def lhas(__obj, x=" "):
    has = 0
    lenx = len(x)
    __obj = __obj[:]
    while __obj.startswith(x):
        has += 1
        __obj = __obj[lenx:]
    return has


def rhas(__obj, x=" "):
    has = 0
    lenx = len(x)
    __obj = __obj[:]
    while __obj.endswith(x):
        has += 1
        __obj = __obj[:-lenx]
    return has


def get_functionInformation(func, hasDecorate=False):
    if not isinstance(func, Callable):
        raise ValueError("func is not Callable")
    try:
        filename = func.__code__.co_filename
        startline = func.__code__.co_firstlineno
    except AttributeError:
        filename = func.__call__.__code__.co_filename
        startline = func.__call__.__code__.co_firstlineno
    endline = startline
    dline = 0
    for encodeing in ("gbk", "utf-8", "utf-16", "ASCII"):
        with open(filename, encoding=encodeing) as file:
            try:
                lines = file.readlines()
            except UnicodeDecodeError:
                pass
            else:
                break
    lhasStratline = lhas(lines[startline - 1])
    while lines[endline - 1].lstrip().startswith("@"):
        endline += 1
        if not hasDecorate:
            startline += 1
        dline += 1
    while lhasStratline < lhas(lines[endline].rstrip()):
        endline += 1
    return (filename, startline, endline, dline)


def toFunc(funcname, file):
    funcname = funcname.strip()
    from importlib import util
    spec = util.spec_from_file_location(_o.path.split(file)[1], file)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return eval("module.%s" % funcname)
    except NameError:
        raise AttributeError("not find attribute " + funcname) from None


class Information:
    def __init__(self, func):
        self.funcname = func.__name__
        self.filename, self.startline, self.endline, self.decorate = get_functionInformation(
            func,
            True,
        )
        self.decorates = []
        with open(self.filename) as file:
            lines = file.readlines()
            for i in range(self.decorate):
                self.decorates.append(
                    Information(
                        toFunc(
                            lines[self.startline + i - 1].lstrip().lstrip("@"),
                            self.filename,
                        ),
                    ),
                )
                self.decorate += 1


def overload_dummy(*funcs, raised=False):
    funcs_parameter = list(_getParameterNames(func) for func in funcs)
    funcs_parameter = tuple(enumerate(funcs_parameter, 1))
    funcs_parameter = list(
        "%s: %s" % (
            i[0],
            ", ".join(i[1]) if i[1] else "No parameters",
        ) for i in funcs_parameter
    )
    funcs_parameter = "\n\t".join(funcs_parameter)
    funcs_parameter = "Unrecognized parameters, parameters is:\n\t" + funcs_parameter
    
    def overloads(*args, **kwargs):
        exc = []
        for func in funcs:
            try:
                return func(*args, **kwargs)
            except TypeError:
                exc.append(_r.format_exc())
        print("Traceback of overload", "Traceback (most recent call last):", "  ValueError: ", end="", sep="\n", file=_s.stderr)
        print(funcs_parameter, file=_s.stderr)
        try:
            print("But your parameters is:", args, kwargs, file=_s.stderr)
        except:
            print("can't print", file=_s.stderr)
        print("\n")
        for e in exc:
            print(e, "\n", file=_s.stderr)
        exit(1)
        
    overloads.__name__ = funcs[0].__name__
    overloads.__qualname__ = funcs[0].__qualname__
    overloads.__module__ = funcs[0].__module__
    return overloads


_overloads = _defaultdict(functools.partial(_defaultdict, tuple))


def has_overloads(func):
    if func.__module__ in _overloads and \
            func.__qualname__ in _overloads[func.__module__]:
        return func in _overloads[func.__module__][func.__qualname__]
    else:
        return False


def overload(*funcs):
    if len(funcs) == 0:
        funcs = (False,)
    if isinstance(funcs[0], bool):
        def overload(func):
            if has_overloads(func) is None:
                _overloads[func.__module__][func.__qualname__] = (func,)
            else:
                _overloads[func.__module__][func.__qualname__] += (func,)
            return overload_dummy(
                *_overloads[func.__module__][func.__qualname__],
                raised=funcs[0],
            )
        return overload
    else:
        for _func in funcs:
            if has_overloads(_func) is None:
                _overloads[_func.__module__][_func.__qualname__] = (_func,)
            else:
                _overloads[_func.__module__][_func.__qualname__] += (_func,)
        return overload_dummy(
            *_overloads[funcs[-1].__module__][funcs[-1].__qualname__],
            raised=False
        )


def clear_overloads(): # don't clear, otherwise, the entire library will crash
    _overloads.clear()


def _getParameterNames(func):
    """Returns a list of parameter names for the given function."""
    signature = _i.signature(func)
    return [param.name for param in signature.parameters.values()]


@overload(True)
def get_overloads(func):
    """Return all defined overloads for *func* as a sequence."""
    # classmethod and staticmethod
    if isinstance(func, Callable):
        f = getattr(func, "__call__", func)
        return get_overloads(f.__module__, f.__qualname__)
    elif isinstance(func, str):
        return get_overloads(*func.rsplit(".", 1))


@overload(True)
def get_overloads(module, qaulname):
    if module not in _overloads:
        return []
    mod_dict = _overloads[module]
    if qaulname not in mod_dict:
        return []
    return mod_dict[qaulname]
    

def is_isAreRaise(_raise=None, name="inited", _is=False, func=None):
    if func is None:
        def _is_isAreRaise(func, __raise=None, _name=None, __is=None):
            return is_isAreRaise(
                __raise if __raise else _raise,
                  _name if   _name else   name,
                   __is if    __is else    _is,
                func,
            )
        _is_isAreRaise.__name__ = is_isAreRaise.__name__
        return _is_isAreRaise
    
    def new(self, *args, **kwargs):
        if getattr(self, name, _is) == _is:
            if isinstance(_raise, BaseException):
                raise _raise
            elif isinstance(_raise, str):
                raise Exception(_raise)
            elif isinstance(_raise, type) and issubclass(_raise, BaseException):
                raise _raise
            elif _raise is None:
                raise Exception
            else:
                raise ValueError("can't identify _raise parameter")
        return func(self, *args, **kwargs)
    
    new.__name__ = func.__name__
    return new


nonefunc = lambda: None
returnselffunc = lambda self: self


def gosuper(name, func):
    def new(self, other):
        return getattr(super(self.__class__, self), name)(func(other))
    new.__name__ = name
    return new


def typegosuper(__type, *args):
    for name, func in args:
        setattr(__type, name, gosuper(name, func))


if __name__ == "__main__":
    @CallWrapper
    def a():
        raise ValueError
    infor = Information(a)
    print(infor.__dict__)
    print(*map(lambda obj: obj.__dict__, infor.decorates))
