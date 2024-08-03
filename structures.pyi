from typing import (
    Any, Callable, Dict, Iterable, List, SupportsIndex, Tuple, Union,
    overload,
)
from func import Count


# indices start with 1


class _Node:
    """Store an object(_obj) and edge, and use add and remove to add or remove edges"""
    ...

_Points = _Node | Iterable[_Points]

class Diagram:
    points: List[_Node]
    
    def __init__(self, *points: _Points) -> None:...
    def swap(self, *points: _Points) -> None:...
    def add(self, *points: _Points) -> None:...
    def remove(self, *points: _Points) -> None:...
    def __len__(self) -> SupportsIndex:...
    def copy(self) -> _Diagram:...
    def __copy__(self) -> _Diagram:...
    def deepsearch(
        self,
        start: _PointType,
        turnback: _Value = ...,
    ) -> Tuple[_PointType]:...
    def breadthfirstsearch(
        self,
        start: _PointType,
        turnback: _Value = ...,
    ) -> Tuple[_PointType]:...

def getfather(x: SupportsIndex, son: SupportsIndex) -> SupportsIndex:...
def getson(x: SupportsIndex, father: SupportsIndex) -> SupportsIndex:... # get min son
def getsonindex(x: SupportsIndex, son: SupportsIndex) -> SupportsIndex:...

class Tree(Diagram):
    head: Any
    wide: SupportsIndex # can't modify
    height: SupportsIndex # can't modify
    father: Tree
    def __init__(self, x: SupportsIndex, point: Any) -> None:...
    def __getitem__(self, item: int) -> Tree | None:...
    def __setitem__(self, key: int, value: Tree | Any) -> None:...
    def __delitem__(self, key: int) -> None:...

class BinaryTree(Tree):
    left: BinaryTree | None
    right: BinaryTree | None
    _x: int = 2
    
    def __init__(self, point: Any) -> None:...
    def preorder(self) -> Tuple[Any]:...
    def postorder(self) -> Tuple[Any]: ...
    def inorder(self) -> Tuple[Any]: ...


class Default:
    _type: List[Any] | Dict[Any]
    value: List[Any] | Dict[Any]
    def __repr__(self) -> str:...
    def __init__(self, _type: Any | type) -> None:...
    def __getitem__(self, item: Any | int) -> Any | Default:...
    def __setitem__(self, key: Any | int, value: Any) -> None:...
    def __delitem__(self, key: Any | int) -> None:...
    def __iter__(self) -> _Iter:...
    def __len__(self) -> int:...
    def __getattribute__(self, item: str) -> Any:...
    def __add__(self, other: Default) -> Default:...
    def __mul__(self, other: _Iter | int) -> Default:...
    def __pow__(self, power) -> Default:...
    def copy(self) -> Default:...
    def __copy__(self) -> Default:...
    if _type == list:
        def append(self, __obj: Any) -> None:...


class Stack:
    top: Any
    empty: bool
    size: int
    def __bool__(self) -> bool:...
    def __len__(self) -> int:...
    def pop(self) -> Any:...
    def push(self, __obj: Any) -> None:...
    def __init__(self) -> None:...
    def __iter__(self) -> _Iter:...
    def __str__(self) -> str:...
    @overload
    def __getitem__(self, item: SupportsIndex) -> Any:...
    @overload
    def __getitem__(self, item: slice) -> Any:...


class Queue:
    top: Any
    empty: bool
    size: int
    def __bool__(self) -> bool:...
    def pop(self) -> Any:...
    def __len__(self) -> int:...
    def push(self, __obj: Any) -> None:...
    def __init__(self) -> None:...
    def __iter__(self) -> _Iter:...
    def __str__(self) -> str:...
    @overload
    def __getitem__(self, item: SupportsIndex) -> Any: ...
    @overload
    def __getitem__(self, item: slice) -> Any: ...

_KeyCall = Callable[[Any, Any], bool]
_LeCall = lambda a, b: a < b

class PileUp(BinaryTree):
    empty: bool
    size: SupportsIndex
    key: _KeyCall
    def __init__(self, key: _KeyCall = _LeCall) -> None:...
    def reverse(self) -> None:...
    def swap(self, *points: Any) -> None:...
    def clear(self) -> None:...
    def update(self) -> None:...
    def __iter__(self) -> Iterable:...
    def __str__(self) -> str:...
    def sort(self, key: _KeyCall | None = None) -> None:...
    def append(self, __obj: Any) -> None:...
    def extend(self, __iter: Iterable[Any]) -> None:...
    def copy(self) -> PileUp:...

class _Find:
    def __iter__(self) -> Iterable:...
    def __len__(self) -> SupportsIndex:...
    def __repr__(self) -> SupportsIndex:...
    def __int__(self) -> SupportsIndex:...

class Avl(BinaryTree):
    def __init__(self, key: _KeyCall = _LeCall) -> None:...
    def append(self, __obj: Any) -> None:...
    def extend(self, __iter: Iterable[Any]) -> None:...
    def find(self, __obj: Any) -> Union[_Find, -1]:...
    def index(self, __obj: Any) -> _Find:...
    def count(self, __obj: Any) -> List[_Find]:...
    def reverse(self) -> None:...
    def swap(self, *points: Any) -> None:...
    def clear(self) -> None:...
    
def treeToTuple(tree: Tree) -> Tuple[Tuple[Any]]:...

class ImmutableObject:
    __count: Count
    def __init__(self) -> None:...
    def __hash__(self) -> int:...
    # __eq__ is a comparison pointer, otherwise an error will occur

class HashList:
    def __init__(self, *adds: Any) -> None:...
    def append(self, *adds: Any) -> None:...
    def has(self, has: Any) -> bool:...
    def remove(self, remove: Any) -> None:...
