import functools
import inspect as _i
import os as _o
import sys as _s
import threading as _t
import time as _d
import traceback as _r
from collections import defaultdict as _defaultdict
# _defaultdict = lambda: _Default(dict)
from typing import Callable


_stdout = _s.stdout


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
    def __init__(self, x, func="__add__"):
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
                self._number,
                value,
                getattr(self._number, "__%s__" % value),
            )
        elif isinstance(value, Callable):
            self._func = value
        else:
            raise ValueError(
                "value parameter be str or Callable, not %s" % type(value).__name__)
    
    @func.deleter
    def func(self):
        raise AttributeError("func atrribute can't delete")
        
    
class CallWrapper:
    def __init__(self, *funcs, newThead=False, raised=False, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        if len(funcs) > 1:
            self.func = overload_dummy(*funcs)
        else:
            self.func = funcs[0]
        self.args   = args
        self.kwargs = kwargs
        self.newThread = newThead
        self.raised = raised
    
    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self, value):
        if not isinstance(value, Callable):
            raise ValueError("value parameter is not a Callable")
        self._inited = True
        self._func = value
        self.__name__ = value.__name__
        self.__code__ = value.__code__
        self.code = value.__code__
        self._inited = True
    
    @func.deleter
    def func(self):
        self._func = None
        self.__name__ = None
        self.__code__ = None
        self.code = None
        self.inited = False
    
    def start(self, *args, **kwargs):
        if not self._inited:
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
            if self.raised:
                raise
            else:
                print("func.py in CallWrapper.__call__", file=_s.stderr)
                lines = _r.format_exc().split("\n")
                print(lines)
                r = lines[-2]
                new = lines[:2]
                pname = _o.getcwd() + r"\pyns\func.py"
                print(pname)
                new = map(
                    lambda _s: _s.replace(
                        pname,
                        "<func>",
                    ).replace(
                        "start",
                        "CallWrapper.start",
                    ),
                    new,
                )
                new = list(new)
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
    func: CallWrapper
    while hasattr(func, "func"):
        old_func, func = func, func.func
        if isinstance(func, property):
            func = func.fget(old_func)
    filename = func.__code__.co_filename
    startline = func.__code__.co_firstlineno
    endline = startline
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
    while lhasStratline < lhas(lines[endline].rstrip()):
        endline += 1
    return (filename, startline, endline)


def toFunc(funcname, file):
    funcname = funcname.strip()
    file_index = 0
    for line in file:
        if funcname in line:
            line = line.strip()
            index = line.index(funcname)
            if line[:index].lstrip() in ("def ", "class "):
                linehas = lhas(line)
                dline = 0
                func_string = ""
                while file[file_index - dline - 1].lstrip().startswith("@"):
                    dline += 1
                    func_string = file[file_index - dline].lstrip() + func_string
                rline = 0
                while linehas < lhas(file[file_index + rline]):
                    func_string += file[file_index + rline]
                    rline += 1
                exec(func_string)
                return eval(funcname)
            elif index == 0 and line[len(funcname):].lstrip()[0] == "=":
                exec(line)
                return eval(funcname)
            file_index += 1
    raise AttributeError("not find attribute " + funcname)


class Information:
    def __init__(self, func):
        self.funcname = func.__name__
        self.filename, self.stratline, self.endline = get_functionInformation(
            func,
            True,
        )
        self.decorate = 0
        self.decorates = []
        with open(self.filename) as file:
            lines = file.readlines()
            while lines[self.stratline + self.decorate - 1].lstrip().startswith("@"):
                self.decorates.append(
                    Information(
                        toFunc(
                            lines[self.stratline + self.decorate - 1].lstrip(
                            ).lstrip("@"),
                            lines,
                        ),
                    ),
                )
                self.decorate += 1


def overload_dummy(*funcs, raised=False):
    if len(funcs) < 1:
        raise ValueError("funcs parameter can't be empty")
    
    funcs_parameter = list(_getParameterNames(func) for func in funcs)
    funcs_parameter = tuple(enumerate(funcs_parameter, 1))
    funcs_parameter = list(
        "%s: %s" % (
            i[0],
            ", ".join(i[1]) if i[1] else "No parameters",
        ) for i in funcs_parameter
    )
    funcs_parameter = ";\n\t".join(funcs_parameter) + "."
    funcs_parameter = "Unrecognized parameters, parameters is:\n\t" + funcs_parameter
    
    def overloads(*args, **kwargs):
        for func in funcs:
            if _validateInput(func, args, kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    filename, startline, endline = get_functionInformation(func)
                    if e.__traceback__.tb_frame.f_globals != filename or \
                            not startline < e.__traceback__.tb_lineno < endline:
                        if raised:
                            raise
                        print(
                            "func.py in overload_dummy",
                            file=_s.stderr,
                        )
                        lines = _r.format_exc().split("\n")
                        r = lines[-2]
                        new = lines[:2]
                        pname = _o.getcwd() + r"\func.py"
                        new = map(
                            lambda _s: _s.replace(
                                pname,
                                "<func>",
                            ).replace(
                                "overloads",
                                "overload_dummy",
                            ),
                            new,
                        )
                        new = list(new)
                        _lines = lines[3:-2]
                        _lines[0] = _lines[0].lstrip().lstrip("^")
                        lines = new + _lines
                        for line in lines:
                            if not line:
                                lines.remove(line)
                        lines = "\n  ".join(lines)
                        lines = "  " + lines
                        lines += "\n" + r
                        print(lines, file=_s.stderr)
                        return
        raise ValueError(funcs_parameter) from None
            
    overloads.__name__ = funcs[0].__name__
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


def _validateInput(func, args, kwargs):
    signature = _i.signature(func)
    try:
        bound_arguments = signature.bind(*args, **kwargs)
    except TypeError:
        return False
    bound_arguments.apply_defaults()
    _empty = _i.signature(lambda s: None)
    empty = _empty.bind("")
    empty = empty.arguments.keys()
    empty = tuple(empty)[0]
    empty = _empty.parameters[empty]
    empty = empty.annotation
    for name, value in bound_arguments.arguments.items():
        parameter = signature.parameters[name]
        if parameter.annotation != empty and not isinstance(value, parameter.annotation):
            return False
    return True


def validate_input(func):
    def wrapper(*args, **kwargs):
        if not _validateInput(func, args, kwargs):
            return
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@overload(True)
def get_overloads(func):
    """Return all defined overloads for *func* as a sequence."""
    # classmethod and staticmethod
    if isinstance(func, Callable) or hasattr(func, "__func__"):
        f = getattr(func, "__func__", func)
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
        pass
    
    infor = Information(a)
    print(infor.__dict__)
