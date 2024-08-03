try:
    from iter import flatten as _fl, toTuple as _tT
    from func import Count as _Count
except ModuleNotFoundError:
    from .iter import flatten as _fl, toTuple as _tT
    from .func import Count as _Count
import re as _re
import sys as _sys


_sys.set_coroutine_origin_tracking_depth(10000)


def pow(base, __x=2):
    return base ** __x


class _Node:
    def __init__(self, __obj, *nodes):
        self._obj = __obj
        self.swap(nodes)
    
    def swap(self, *nodes):
        self._connect = []
        self.add(nodes)
    
    def __get__(self, instance, owner):
        return self._obj
    
    def __set__(self, instance, value):
        self._obj = value
    
    def __del__(self):
        self.remove(self._connect)
        del self._obj
    
    def __getattribute__(self, item):
        if item in ("copy", "add", "remove", "__get__", "__set__", "__del__", "__init__"):
            return super(_Node, self).__getattribute__(item)
        else:
            return getattr(self._obj, item)
    
    def copy(self):
        import copy
        return self.__class__(copy.copy(self._obj), self._connect.copy())
    
    def add(self, *nodes):
        self._aor("append", nodes)
    
    def remove(self, *nodes):
        self._aor("remove", nodes)
    
    def _aor(self, key, args):
        def succes(arg):
            if (arg in self._connect and self in arg._connect) or key == "append":
                getattr(self._connect, key)(arg)
                getattr(arg._connect, key)(self)
            else:
                raise ValueError("arg must be in self and self must be in arg")
        
        def fail():
            raise TypeError(
                "the arg must to be Node or Iterable[arg to be], not ",
                type(arg).__name__,
            )
        
        from typing import Iterable
        for arg in args:
            if isinstance(arg, _Node):
                succes(arg)
                continue
            if isinstance(arg, Iterable):
                try:
                    self._aor(key, arg)
                except (TypeError, ValueError):
                    pass
                else:
                    continue
            if key == "remove":
                flag = False
                for c in self._connect:
                    if c == arg:
                        succes(c)
                        flag = True
                        break
                if flag:
                    continue
            fail()


class Diagram:
    def __init__(self, *points):
        self.swap(points)
    
    def swap(self, *points):
        self.points = []
        self.add(points)
    
    def copy(self):
        return self.__class__(self.points)
    
    def __copy__(self):
        return self.copy()
    
    def __set__(self, instance, value):
        self.swap(value)
    
    def __get__(self, instance, owner):
        return self.points
    
    def clear(self):
        self.points.clear()
    
    def add(self, *points):
        self._aor("append", points)
    
    def remove(self, *points):
        self._aor("remove", points)
    
    def _aor(self, key, args):
        def succes(arg):
            if arg in self.points or key == "append":
                getattr(self.points, key)(arg)
            else:
                raise ValueError("arg must be in self")
        
        from typing import Iterable
        for arg in args:
            if isinstance(arg, _Node):
                succes(arg)
                continue
            if isinstance(arg, Iterable):
                try:
                    self._aor(key, arg)
                except (TypeError, ValueError):
                    pass
                else:
                    continue
            if key == "remove":
                flag = False
                for node in self.points:
                    if node == arg:
                        succes(c)
                        flag = True
                        break
                if flag:
                    continue
            succes(_Node(arg))
    
    def __len__(self):
        return len(self.points)
    
    def __iter__(self):
        return iter(self.points)
    
    def deepsearch(self, start):
        vis = []
        for obj in self.points:
            if obj._obj == start:
                start = obj
                break
        
        def dfs(x):
            if x in vis:
                return []
            vis.append(x)
            temp = [x]
            for v in x._connect:
                temp.extend(dfs(v))
            return temp
        return dfs(start)
    
    def breadthfirstsearch(self, start):
        vis = []
        for obj in self.points:
            if obj._obj == start:
                start = obj
                break
        q = Queue()
        q.push(start)
        while not q.empty:
            u = q.pop()
            vis.append(u)
            for v in u._connect:
                if v not in vis:
                    q.push(v)
        return vis
    
    def __bool__(self):
        return bool(self.points)


class TreeError(Exception):
    pass


class EmptyError(Exception):
    def __init__(self, arg):
        super(EmptyError, self).__init__(
            "the %s object is empty, it can't be empty" % arg.__class__.__name__)


class TreeEmptyError(TreeError, EmptyError):
    def __init__(self, arg):
        if not issubclass(arg, Tree):
            raise TypeError("the arg of TreeEmptyError must be Tree subclass")
        EmptyError.__init__(self, arg)


def getfather(x, son):
    if x == 1:
        return son - 1
    return son // x + int(son % x >= 2)


def getson(x, father):
    return (father - 1) * x + 2


def getsonindex(x, son):
    return ((son + 2) % x if (son + x) % x > 0 else x)


class Tree(Diagram):
    def __bool__(self):
        return self._obj is not None
    
    def __len__(self):
        return sum(
            map(
                lambda x: 0 if x is None else len(x),
                self._trees[1:]
            )
        ) + int(self.head is not None)
    
    def __iter__(self):
        temp = []
        if self.head is not None:
            temp.append(self.head)
            for tree in self._trees:
                if tree is not None:
                    temp.extend(iter(tree))
        return iter(temp)
    
    def __str__(self):
        return str(tuple(self))
    
    @property
    def head(self):
        return self._obj
    
    @head.setter
    def head(self, value):
        self._obj = value
    
    @property
    def wide(self):
        return self._x
    
    @property
    def height(self):
        return self._h + 1
    
    @property
    def father(self):
        return self._father
    
    @father.setter
    def father(self, value):
        if self._father is not None:
            self._father._h = self.__h
        self._father = value
        self.__h = self._father.height
        if value.height > self._h:
            self._h = value.height

    def __init__(self, x, point):
        if point is None and not isinstance(self, _EBTree):
            raise TreeEmptyError(self.__class__)
        self._x = x
        self._h = 0
        self.__h = 0
        self.clear()
        self._obj = point
        self._father = None
    
    def copy(self):
        temp = self.__class__(self._x, self._obj)
        temp.swap(self)
        return temp
    
    def clear(self):
        self._trees = [None] * (self._x + 1)
        self._obj = None
    
    def swap(self, tree):
        self._x = tree.wide
        self._obj = tree.head
        self._h = tree.height
        for i in range(1, self._x + 1):
            self._trees[i] = tree[i].copy()
    
    def __get__(self, instance, owner):
        return self._obj
    
    def __set__(self, instance, value):
        self._obj = value
    
    def __getattr__(self, item):
        if item == "_obj":
            return getattr(super(Tree, self), item)
        return getattr(self._obj, item)
    
    def __getitem__(self, item):
        if item == 0:
            return self._obj
        if item > self._x:
            temp = self[getfather(self._x, item)][getsonindex(self._x, item)]
        else:
            temp = self._trees[item]
            if temp is None and isinstance(self, _EBTree):
                temp = self._trees[item] = self.__class__(self.key)
                temp.father = self
        return temp
    
    def __setitem__(self, key, value):
        if key == 0:
            self._obj = value
        if self[key].father is self:
            self[key].father = None
        if value is None:
            return
        if not isinstance(value, self.__class__):
            if isinstance(self, _EBTree):
                temp, value = value, self.__class__(self.key)
                value.append(temp)
            else:
                value = self.__class__(self._x, value)
        value.father = self
        if item >= self._x:
            self[getfather(self._x, key)][getsonindex(self._x, key)] = value
        else:
            self._trees[key] = value
    
    def __delitem__(self, key):
        self[key] = None
    
    
def _mp(key, index):
    if key == "set":
        return lambda self, value: self.__setitem__(index, value)
    else:
        return lambda self: getattr(self, "__%sitem__" % key)(index)


def _mpr(index):
    return property(_mp("get", index), _mp("set", index), _mp("del", index))
    
    
class BinaryTree(Tree):
    def __setitem__(self, key, value):
        if not isinstance(value, self.__class__):
            if isinstance(self, _EBTree):
                temp, value = value, self.__class__(self.key)
                value.append(temp)
            else:
                value = self.__class__(value)
        super(BinaryTree, self).__setitem__(key, value)
    
    left = _mpr(1)
    right = _mpr(2)
    
    def __init__(self, point):
        super(BinaryTree, self).__init__(2, point)
    
    def preorder(self):
        temp = ()
        temp += (self._obj,)
        left = self.left
        if left:
            temp += left.preorder()
        right = self.right
        if right:
            temp += right.preorder()
        return temp
    
    def inorder(self):
        if not self:
            print(id(self))
            return ()
        temp = ()
        if self._trees[0] is not None:
            temp += self.left.inordertraversal()
        temp += (self.head,)
        if self._trees[1] is not None:
            temp += self.right.inordertraversal()
        return temp
    
    def postorder(self):
        temp = ()
        left = self.left
        if left:
            temp += left.postordertraversal()
        right = self.right
        if right:
            temp += right.postordertraversal()
        temp += (self.head, )
        return temp


class Default:
    def __repr__(self):
        return repr(self._type)
    
    def __init__(self, _type):
        if not isinstance(_type, type):
            self.type = type(_type)
            self._type = _type
            return
        if _type not in (dict, list):
            raise ValueError("_type to be dict or list, not %s" % _type.__name__)
        self.type = _type
        self._type = _type()
    
    def __getitem__(self, item):
        try:
            return self._type[item]
        except (KeyError, IndexError):
            if self.type == dict:
                self._type[item] = Default(self.type)
            else:
                for _ in range(len(self), item + 1):
                    self._type.append(Default(self.type))
            return self._type[item]
    
    def __setitem__(self, key, value):
        if self.type == dict:
            self._type[key] = value
        else:
            for _ in range(len(self), key + 1):
                self._type.append(Default(self.type))
            self._type[key] = value
    
    def __delitem__(self, key):
        del self._type[key]
    
    def __iter__(self):
        return iter(self._type)
    
    def __len__(self):
        return len(self._type)
    
    def __getattribute__(self, item):
        if item in ("__dict__", "copy", "value") or item in self.__dict__.keys():
            return super(Default, self).__getattribute__(item)
        else:
            return getattr(self._type, item)
    
    def __add__(self, other):
        if not isinstance(other, type(self)) or other.type != self.type:
            raise TypeError(
                "can't + to %s and %s" % (
                    self.__class__.__name__,
                    other.__class__.__name__,
                ),
            )
        temp = Default(self.type)
        temp._type = self._type + other._type
        return temp
    
    def __mul__(self, other):
        temp = Default(self.type)
        for _ in (range(other) if isinstance(other, int) else other):
            temp += self
        return temp
    
    def __pow__(self, power):
        temp = self.copy()
        for _ in range(power - 1):
            temp *= self
        return temp
    
    def copy(self):
        temp = Default(self.type)
        temp._type = self._type
        return temp
    
    __copy__ = copy
    
    @property
    def value(self):
        return self._type


class Stack:
    def __bool__(self):
        return bool(self._list)
    
    def __init__(self):
        self._list = []
        
    @property
    def top(self):
        if self.empty:
            raise EmptyError(self)
        return self._list[-1]
    
    @property
    def empty(self):
        return not self._list
    
    @property
    def size(self):
        return len(self._list)
    
    def __len__(self):
        return self.size
    
    def push(self, __obj):
        self._list.append(__obj)
    
    @top.setter
    def top(self, __obj):
        self.push(__obj)
    
    def pop(self):
        if self.empty:
            raise EmptyError(self)
        return self._list.pop()
    
    def __iter__(self):
        return iter(reversed(self._list))
    
    def __str__(self):
        return str(list(self))
    
    def __getitem__(self, item):
        return self._list[item]


class Queue:
    def __bool__(self):
        return bool(self._list)
    
    def __init__(self):
        self._list = []
    
    @property
    def top(self):
        if self.empty:
            raise EmptyError(self)
        return self._list[0]
    
    def pop(self):
        if self.empty:
            raise EmptyError(self)
        return self._list.pop(0)
    
    def push(self, __obj):
        self._list.append(__obj)
    
    @property
    def empty(self):
        return not self._list
    
    @property
    def size(self):
        return len(self._list)
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return self._list
    
    def __str__(self):
        return str(list(self))
    
    def __getitem__(self, item):
        return self._list.__getitem__(item)


class _EBTree(BinaryTree):
    def __init__(self, key=lambda a, b: a < b):
        self.key = key
        super(_EBTree, self).__init__(None)

    def extend(self, __iter):
        for __obj in __iter:
            self.append(__obj)
    
    def reverse(self):
        old_key, self.key = self.key, lambda a, b: not old_key(a, b)
        self.swap(*iter(self))
    
    def swap(self, *points):
        self.clear()
        self.extend(points)
    
    def sort(self, key):
        self.key = key
        self.swap(*iter(self))


class PileUp(_EBTree):
    @property
    def empty(self):
        return self.size == 0
    
    @property
    def size(self):
        return len(self)
    
    def _swap(self, x, y):
        self[x], self[y] = self[y], self[x]
    
    def append(self, __obj):
        self.points_list.append(__obj)
        x = self.size
        while x >= 1 and self.key(__obj, self[x // 2]):
            self._swap(x, x // 2)
            x //= 2
    

class _Find:
    def __init__(self):
        self.__l = []
    
    def __iter__(self):
        return iter(self.__l)
    
    def __repr__(self):
        return "route: %s, index: %d" % (" ".join(map(str, self.__l)), int(self))
    
    def __int__(self):
        i = 1
        for x in self.__l:
            i += i + x
        return i - 1
    
    def insert(self, x):
        self.__l.insert(0, x)


class _Avl(_EBTree):
    def remove(self, *objs):
        for obj in objs:
            temp = list(self.find(obj))
            tree = self
            for x in temp:
                tree = tree[x+1]
            del tree[0]
            while tree:
                if tree.left.height >= tree.right.height:
                    tree = tree.left
                else:
                    tree = tree.right
    
    def append(self, __obj):
        if self.head is None:
            self.head = __obj
            return
        if self.key(__obj, self.head):
            self.left.append(__obj)
        else:
            self.right.append(__obj)
        self._rotate()
    
    def find(self, __obj):
        if self.head is None:
            return []
        if self.head == __obj:
            return _Find()
        if not self.key(__obj, self.head):
            temp = self.right.find(__obj)
            if temp != -1:
                temp.insert(1)
                return temp
        else:
            temp = self.left.find(__obj)
            if temp != -1:
                temp.insert(0)
                return temp
        return -1
    
    def index(self, __obj):
        temp = self.find(__obj)
        if isinstance(temp, _Find):
            return temp
        else:
            [].index(__obj)
    
    def count(self, __obj):
        t = []
        if self.head is None:
            return []
        if self.head == __obj:
            return [_Find()]
        if self.key(__obj, self.head):
            temp = self.left.count(__obj)
            for x in temp:
                x.insert(0)
            return temp
        else:
            temp = self.right.count(__obj)
            for x in temp:
                x.insert(1)
            return t + temp
    
    def _leftrotate(self):
        right = self.right
        self.right = right.left
        if self.father.left == self:
            self.father.left = right
        else:
            self.father.right = right
        self.father = right
    
    def _rightrotate(self):
        left = self.left
        self.left = left.right
        if self.father.left == self:
            self.father.left = left
        else:
            self.father.right = left
        self.father = left
    
    def _rotate(self):
        if abs(self.left.height - self.right.height) <= 1:
            return
        if self.left.height > self.right.height:
            if self.left.left.height < self.left.right.height:
                self.left._leftrotate()
            self._rightrotate()
        else:
            if self.right.right.height < self.right.left.height:
                self.right._rightrotate()
            self._leftrotate()
    
    def __iter__(self):
        return iter(self.inorder())

    def __contains__(self, item):
        return self.find(item) != -1


class Avl:
    @property
    def key(self):
        return self._avl.key
    
    @key.setter
    def key(self, value):
        self.sort(value)
    
    def __init__(self, key=lambda a, b: a < b):
        self._avl = _Avl(key)
    
    def append(self, __obj):
        self._avl.append(__obj)
        while self._avl.father is not None:
            self._avl = self._avl.father
    
    def extend(self, __iter):
        self._avl.extend(__iter)
        while self._avl.father is not None:
            self._avl = self._avl.father
    
    def sort(self, key):
        self._avl.sort(key)
    
    def reverse(self):
        self._avl.reverse()
    
    def preorder(self):
        return self._avl.preorder()
    
    def postorder(self):
        return self._avl.postordertraversal()
    
    def inorder(self):
        return self._avl.inorder()
    
    def __iter__(self):
        return self._avl.__iter__()
    
    def __get__(self, instance, owner):
        return self._avl
    
    def __contains__(self, item):
        return self._avl.__contains__(item)
    
    def count(self, __obj):
        return self._avl.count(__obj)
    
    def __getitem__(self, item):
        return self._avl.__getitem__(item)
    
    def __setitem__(self, key, value):
        self._avl.__setitem__(key, value)
    
    def __delitem__(self, key):
        self._avl.__delitem__(key)
    
    @property
    def left(self):
        return self._avl.left
    
    @left.setter
    def left(self, value):
        self._avl.left = value
    
    @left.deleter
    def left(self):
        del self._avl.left
    
    @property
    def right(self):
        return self._avl.left
    
    @right.setter
    def right(self, value):
        self._avl.left = value
    
    @right.deleter
    def right(self):
        del self._avl.left
    
    @property
    def height(self):
        return self._avl.height
    
    @property
    def head(self):
        return self._avl.head
    
    @property
    def wide(self):
        return self._avl.wide
    
    def __subclasscheck__(self, subclass):
        return\
            isinstance(super(self.__class__, self), subclass) or \
            issubclass(_Avl, subclass) or \
            type(subclass) is self.__class__
    
    def __instancecheck__(self, instance):
        return issubclass(self.__class__, type(instance))
    

class ImmutableObject:
    __count = _Count(0)
    
    def __init__(self):
        self.__hash = next(ImmutableObject.__count)
    
    def __hash__(self):
        return self.__hash


class HashList:
    def __init__(self, *adds):
        self._dict = {}
        self.add(*adds)
    
    def append(self, *adds):
        for obj in adds:
            self._dict[obj] = True
    
    def has(self, has):
        return has in self._dict
    
    def remove(self, *removes):
        for obj in removes:
            del self._dict[obj]


def treeToTuple(tree):
    temp = []
    for i in range(tree.height):
        temp.append([])
        for j in range((i**tree.wide-1) // (tree.wide-1)+1, ((i+1)**tree.wide-1) // (tree.wide-1)+1):
            temp[-1].append(tree[j])
        temp[-1] = tuple(temp[-1])
    return tuple(temp)
    

PREFIX = "prefix"
SUFFIX = "suffix"
INFIX  = "infix"
operator_level = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'log': 4, '!': 5}


def isnumber(number):
    zf = "[-+]"
    d = fr"[-+]?\d*\.?\d*([eE]\d*\.?\d*)?|[a-zA-Z_]\w*"
    digit = f"({d}+|{d}+.{d}+|.{d}+|{d}+.)"
    digit = f"{zf}?{digit}"
    e = f"([eE]+{digit}+)"
    return bool(_re.fullmatch(f"{zf}?{digit}+{e}?", number))


def tokenize(expression):
    floater = r"[-+]?\d+(\.\d*)?"
    integer = r"[-+]?\d+"
    num = fr"{floater}([eE]{integer})?"
    complexer = fr"{num}([-+]{num}[ijIJ])?"
    operator = r"(?<=\d)[+\-](?=\d)"
    oo = r"[/*^!()]"
    tokens = _re.findall(
        fr"({operator}|{complexer}|{oo}|{floater}|{integer}|[a-zA-Z_]\w*)",
        expression,
    )
    tokens = [token[0] for token in tokens if token[0]]
    print(expression, tokens, "tokenize")
    return tokens


def _isOperator(token):
    return token in ['+', '-', '*', '/', '^', "log", "**"]


def isOperator(token):
    return token in ['+', '-', '*', '/', '^', "log", '!', "**"]


def _er():
    raise SyntaxError("parameter is not expression")


def checkExpressionType(expression):
    if not isinstance(expression, str):
        expression = toString(expression)
    tokens = tokenize(expression)
    if not tokens:
        raise SyntaxError("expression is empty")
    first_token = tokens[0]
    last_token = tokens[-1]

    if _isOperator(first_token) and not _isOperator(last_token):
        return PREFIX
    elif not _isOperator(first_token) and _isOperator(last_token):
        return SUFFIX
    elif not _isOperator(first_token) and not _isOperator(last_token):
        return INFIX
    else:
        _er()


def toInfix(expression):
    if not isinstance(expression, str):
        expression = toString(expression)
    tokens = tokenize(expression)
    et = checkExpressionType(expression)
    if et == INFIX:
        return _tT(tokens)
    stk = Stack()
    for token in reversed(tokens) if et == PREFIX else tokens:
        if token == "!":
            if stk.empty:
                _er()
            arg = stk.pop()
            stk.push((arg, token))
        elif _isOperator(token):
            if stk.size < 2:
                _er()
            if et == PREFIX:
                left = stk.pop()
                right = stk.pop()
            else:
                right = stk.pop()
                left = stk.pop()
            stk.push((left, token, right))
        else:
            stk.push(token)
    if stk.size != 1:
        _er()
    return stk[0]


def toString(expression):
    if isinstance(expression, str):
        return expression
    if isinstance(expression, (tuple, list)):
        return str(expression).replace(",", "").replace("'", "")[1:-1]


def toSuffix(expression):
    if not isinstance(expression, str):
        expression = toString(expression)
    tokens = tokenize(expression)
    et = checkExpressionType(expression)
    if et == SUFFIX:
        return _tT(tokens)
    if et == PREFIX:
        return toSuffix(toInfix(expression))
    temp = []
    stk = Stack()
    for token in tokens:
        if isnumber(token):
            temp.append(token)
        elif token == '(':
            stk.push(token)
        elif token == ')':
            while not stk.empty and stk.top != '(':
                temp.append(stk.pop())
            stk.pop()
        else:
            while not stk.empty and (stk.top != '(' and
                    operator_level[stk.top] >= operator_level[token]):
                temp.append(stk.pop())
            stk.push(token)
    while not stk.empty:
        if stk.top == '(':
            _er()
        temp.append(stk.pop())
    return tuple(temp)


def toPrefix(expression):
    if not isinstance(expression, str):
        expression = toString(expression)
    tokens = tokenize(expression)
    et = checkExpressionType(expression)
    if et == PREFIX:
        return _tT(tokens)
    if et == SUFFIX:
        return toPrefix(toInfix(expression))
    temp = []
    stk = Stack()
    for token in reversed(tokens):
        if isnumber(token):
            temp.append(token)
        elif token == ')':
            stk.push(token)
        elif token == '(':
            while not stk.empty and stk.top != ')':
                temp.append(stk.pop())
            stk.pop()
        else:
            while not stk.empty and (stk.top != ')' and
                    operator_level[stk.top] >= operator_level[token]):
                temp.append(stk.pop())
            stk.push(token)
    while not stk.empty:
        if stk.top == ')':
            _er()
        temp.append(stk.pop())
    return tuple(reversed(temp))
        

class Expression(BinaryTree):
    def __init__(self, expression):
        expression = toString(toInfix(toString(expression)))
        print(expression)
        self._list = []
        nex = ""
        si = 0
        for token in tokenize(expression):
            print(token)
            if isinstance(token, int) or \
                    _re.fullmatch(r"[-+]?\d*\.?\d*([eE]\d*\.?\d*)?", token):
                nex += "array_%d" % len(self._list)
                self._list.append(token)
            else:
                nex += token
        infix = list(nex.replace("(", "").replace(")", ""))
        suffix = list(toSuffix(nex))
        print(infix, suffix)
        super(Expression, self).__init__(suffix.pop())
        if not isnumber(self.head):
            self.left = Expression(infix[:infix.index(self.head)])


if __name__ == '__main__':
    print(Expression("(1+1)*2+2!"))
