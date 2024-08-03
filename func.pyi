import threading
from _io import TextIOWrapper
from typing import (
    Any, Callable, Dict, Iterable, List,
    overload as _overload,
)


_CountFunc = Callable[[Any], Any]
_AllCallable = Callable[[Any, ...], Any]
_CountInputFunc = _CountFunc | str
def flash_print(
        *values: Iterable[Any, ...],
        sep: str = " ",
        file: TextIOWrapper = ...,
        delay: int = 0,
        end: str = "\n",
        new_thread: bool = True
) -> None:...

class Count:
    _func: _CountFunc
    _number: Any
    def __init__(self, x: Any, func: _CountInputFunc = ...) -> None:...
    def __iter__(self) -> Count:...
    def __next__(self) -> Any:...
    @property
    def func(self) -> _CountFunc:...
    @func.setter
    def func(self, value: _CountInputFunc) -> None:...
    @func.deleter
    def func(self) -> None:... # to raise

class CallWrapper:
    _inited: bool
    args: tuple
    kwargs: dict
    newThead: bool
    raised: bool
    
    def __init__(
            self,
            *funcs: _AllCallable,
            newTread: bool = False,
            raised: bool = False,
            args: tuple = (),
            kwargs: dict = {},
    ) -> None:...
    def start(self, *args: Any, **kwargs: Any) -> Any:...
    __call__ = start
    
    @property
    def func(self) -> _AllCallable: ...
    @func.setter
    def func(self, value: _AllCallable) -> None: ...
    @func.deleter
    def func(self) -> None: ... # if start now to raise

class Thread(threading.Thread):
    event: threading.Event
    def __init__(
        self,
        func,
        *,
        addself: False | int = 0,
        name: str | None = ...,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = ...,
        daemon: bool | None = ...,
    ) -> None:...
    def stop(self) -> None:...

_overloads: Dict[str, _AllCallable]
def overlod_dummy(*func: _AllCallable) -> _AllCallable:...
def lhas(__obj: str, x: str) -> int:...
def rhas(__obj: str, x: str) -> int:...
def clear_overloads() -> None:...
def has_overloads(func: _AllCallable) -> bool:...
@_overload
def get_overloads(func: _AllCallable) -> List[_AllCallable]:...
@_overload
def get_overloads(module: str, qaulname: str) -> List[_AllCallable]:...
@_overload
def get_overloads(name: str) -> List[_AllCallable]:...
@_overload
def overload(*func: _AllCallable) -> _AllCallable:...
@_overload
def overload(raised: bool) -> Callable[[_AllCallable], _AllCallable]:...
@_overload
def is_isAreRaise(
        _raise: type | str | None = None,
        name: str = "inited",
        _is: Any = False,
) -> Callable[[_AllCallable, Any, ...], _AllCallable]:...
@_overload
def is_isAreRaise(
        _raise: type | str | None = None,
        name: str = "inited",
        _is: Any = False,
        func: _AllCallable | None = ...,
) -> _AllCallable:...

def nonefunc() -> None:...
def returnselffunc(self: Any) -> Any:...
def gosuper(name: str, func: Callable[[Any], Any]) -> Callable[[Any, Any], Any]:...
def typegosuper(__type: type, *args: Iterable[str, Callable[[Any], Any]]) -> None:...
    