import math as _math, cmath as _cmath
from decimal import Decimal as _Decimal
from math import *
from cmath import *
import re as _re
from copy import copy as _cpy
try:
    from .func import lhas as _lhas, overload as _overload, rhas as _rhas
    from .structures import HashList as _HashList, BinaryTree as _BTree, Stack as _Stk, Queue as _Q
except ImportError:
    from func import lhas as _lhas, overload as _overload, rhas as _rhas
    from structures import HashList as _HashList, BinaryTree as _BTree, Stack as _Stk, Queue as _Q


def sqrt(x):
    temp = _cmath.sqrt(x)
    if temp.imag == 0:
        return temp.real
    else:
        return Complex(temp)


def isEvenNumber(x):
    return x % 2 == 0


def isOddNumber(x):
    return x % 2 != 0


prime = _HashList()
composite = _HashList()


def BOS_min(a, x):
    l = 0
    r = len(a) - 1
    ans = -1
    while l <= r:
        mid = (l + r) // 2
        if a[mid] == x:
            ans = mid
        if a[mid] <= x:
            r = mid - 1
        else:
            l = mid + 1
    return ans


def BOS_max(a, x):
    l = 0
    r = len(a) - 1
    ans = -1
    while l <= r:
        min = (l + r) // 2
        if a[mid] == x:
            ans = mid
        if a[mid] >= x:
            l = mid + 1
        else:
            r = mid - 1
    return ans


def isPrime(x):
    if x == 1:
        return False
    elif x in prime:
        return True
    elif x in composite:
        return False
    for i in range(2, int(sqrt(x))):
        if x % i == 0:
            composite.append(x)
            return False
    prime.append(x)
    return True


def isComposite(x):
    if x == 1:
        return False
    return not isPrime(x)


def update_prime(x):
    x += 1
    is_Prime = [True] * (x+1)
    for i in range(2, x):
        if is_Prime[i]:
            if i not in prime:
                prime.add(i)
            for j in range(i * 2, x+1, i):
                is_Prime[j] = False
        elif i not in composite:
            composite.add(i)
    return is_Prime


update_prime(1000)

isEven = even = isEvenNumber
isOdd  = odd  = isOddNumber

Nmor  = (
    "个",
    "万",
    "亿",
    "兆",
    "京",
    "秭",
    "穰",
    "沟",
    "涧",
    "正",
    "载",
    "极",
    "恒河沙",
    "阿僧祗",
    "那由他",
    "不可思议",
    "无量大海",
    "大数",
    "全仕祥",
    "无量大数",
)
_nmor = ("",) + Nmor[1:]
Sbq   = ("千", "百", "十", "个")
Sbqb  = ("仟", "佰", "拾", "个")
Sbqz  = ("阡", "陌", "拾", "个")
_sbq = Sbq[:-1] + ("",)
Ns    = ("零", "一", "二", "三", "四", "五", "六", "七", "八", "九")
Nsb   = ("零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖")


def pronounce(x, s=_sbq, n=Ns, m=_nmor):
    if x == 0:
        return n[0]
    ans = ""
    c = 0
    mlen = len(m)
    mods = 10 ** len(s)
    while x:
        if c >= mlen:
            raise ValueError(
                "Exceeds the limit (%d digits) for number pronounce conversion"
                ", you can expand Numerical order('m' parameter)" % (mlen * 4))
        temp = x % mods
        x //= mods
        ret = ""
        temp = str(temp).rjust(len(s), "0")
        for i in range(len(s)):
            if token == "0":
                if ret == "" or  ret[-1] != n[0]:
                    ret += n[0]
            else:
                ret += n[int(token)]
                ret += s[i]
        if ret != n[0]:
            if _rhas(ret, n[0]):
                ret = ret[:-1]
            ret += m[c]
        ans = ret + ans
        c += 1
    while _rhas(ans, n[0]):
        ans = ans[:-1]
    while _lhas(ans, n[0]):
        ans = ans[1:]
    temp = ans[:]
    ans = ""
    for c in temp:
        if c == n[0]:
            if ans == "" or ans[-1] != n[0]:
                ans += n[0]
        else:
            ans += c
    if ans.startswith(n[1] + s[2]):
        ans = ans[1:]
    return ans


def number(x, s=_sbq, n=Ns, m=_nmor):
    if x == n[0]:
        return 0
    splits = []
    maxstr = 0
    for stri in m:
        temp = len(stri)
        if temp > maxstr:
            maxstr = temp
    temp = ""
    xlen = len(x)
    c = 0
    while c < xlen:
        for j in range(min(maxstr, xlen - c), 0, -1):
            if x[c:c+j] in m:
                splits.append((temp, m.index(x[c:c+j])))
                temp = ""
                c += j
                break
        else:
            temp += x[c]
            c += 1
    splits.append((temp, 0))
    ans = ""
    c = 0
    for num, j in reversed(splits):
        if j > c:
            ans = (j - c) * "0000" + ans
        c = j + 1
        if num == "":
            ans = "0000" + ans
            continue
        else:
            ret = ""
            for i in range(len(s)-1):
                if s[i] in num:
                    if i == 2 and num.index(s[i]) == 0:
                        ret += "1"
                    else:
                        ret += str(n.index(num[num.index(s[i])-1]))
                else:
                    ret += "0"
            if num[-1] in n:
                ret += str(n.index(num[-1]))
            else:
                ret += "0"
            ret = ret.rjust(len(s), "0")
            ans = ret + ans
    return int(ans)


DEGREES = "degrees"
RADIANS  = "radians"


class Angle:
    def __init__(self, types, number):
        if types == DEGREES:
            self.degrees = number
        elif isinstance(number, complex) and number.imag != 0:
            raise TypeError("number parameter must be float")
        else:
            self.degrees = degrees(number.real)
    
    @property
    def degrees(self):
        return self._degrees
    
    @degrees.setter
    def degrees(self, value):
        self._degrees = value
        self._degrees = fmod(self._degrees, 360)
    
    @property
    def radians(self):
        return radians(self.degrees)
    
    @radians.setter
    def radians(self, value):
        self.degrees = degrees(value)
        
    def __delattr__(self, item):
        raise AttributeError("%s object can't del attribute" % self.__class__.__name__)
    
    def __float__(self):
        return self.degrees
    
    def __int__(self):
        return int(float(self))
    
    def __repr__(self):
        return "%.2f°" % float(self)
    
    def __add__(self, other):
        return Angle(DEGREES, self.degrees + other.degrees)
    
    def __sub__(self, other):
        return Angle(DEGREES, self.degrees - other.degrees)
    
    def __neg__(self):
        return Angle(DEGREES, - self.degrees)
    
    def __truediv__(self, other):
        if isinstance(other, Angle):
            return self.radians / other.radians
        return Angle(RADIANS, self.radians / other)
     
    def __mul__(self, other):
        return Angle(RADIANS, self.radians * other)
    
    def sin(self):
        return sin(self.radians)
    
    def cos(self):
        return cos(self.radians)
    
    def tan(self):
        return tan(self.radians)


@_overload
def numbers(start, number, step=1):
    return range(start, number * step + start, step)


@_overload
def numbers(number):
    return range(number)


IMAG = "imag"
REAL = "real"


def eq(a, b, accuracy=1e-4):
    return abs(a-b) < accuracy


class Complex:
    def __instancecheck__(self, instance):
        if isinstance(instance, complex):
            return True
        return issubclass(type(instance), self.__class__)
    
    def __add__(self, other):
        other = Complex(other)
        return Complex(self.complex + other.complex)
    
    def __radd__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) + self.complex)
        else:
            return NotImplemented
    
    def __sub__(self, other):
        other = Complex(other)
        return Complex(self.complex - other.complex)
    
    def __rsub__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) - self.complex)
        else:
            return NotImplemented
    
    def exp(self):
        return Complex(e ** self)

    def pow(self, other):
        other = Complex(other)
        temp = self.complex
        temp **= other.complex
        return Complex(temp)
    
    __pow__ = pow
    
    def copy(self):
        return Complex(self.complex)
    
    __copy__ = copy
    
    def __abs__(self):
        return abs(complex(self))
    
    def __complex__(self):
        return complex(self.complex)
    
    @_overload
    def __init__(self, __obj):
        if isinstance(__obj, (list, tuple)):
            self.__init__(*__obj)
            return
        if isinstance(__obj, str):
            __obj = __obj.replace(" ", "")
            __obj = __obj.replace("i", "j")
            __obj = __obj.replace("I", "J")
            __obj = __obj.replace("J", "j")
        try:
            self.complex = complex(__obj)
        except:
            raise TypeError("__obj must be comlex, str, int, float, list or tuple, not %s" % type(__obj)) from None
        
    @_overload
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length
    
    @_overload
    def __init__(self, real, imag):
        self.complex = (real, imag)
    
    @_overload
    def __init__(self, types, number, length):
        self.__init__(Angle(types, number), length)
    
    def __repr__(self):
        return str(self.complex)
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        if isinstance(value, Angle):
            if isinstance(value.radians, (int, float)):
                self._angle = value
            elif isinstance(value.radians, (complex, Complex)):
                r = value.radians
                r = complex(r)
                length = e ** - r.imag
                self.length *= length
            self._angle = value
        elif isinstance(value,  (list, tuple)):
            self.angle = Angle(*value)
        else:
            raise TypeError("value must be Angle object or list or tuple")
    
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        if isinstance(value, (int, float)):
            if value < 0:
                value = - value
                self.angle.radians = - self.angle.radians
            self._length = value
        elif isinstance(value, (complex, Complex)):
            value = Complex(value)
            self.angle += value.angle
            self._length = value
        else:
            raise TypeError("value must be int or float")
    
    @property
    def imag(self):
        return self.complex.imag
    
    @imag.setter
    def imag(self, value):
        if isinstance(value, (complex, Complex)):
            self.complex = (self.real, value.real)
            return
        self.complex = (self.real, value)
    
    @property
    def real(self):
        return self.complex.real
    
    @real.setter
    def real(self, value):
        if isinstance(value, (complex, Complex)):
            self.complex = (value.real, self.imag)
            return
        value = value
        self.complex = (value, self.imag)
    
    @property
    def complex(self):
        return self.length * exp(self.angle.radians * 1j)
    
    @complex.setter
    def complex(self, value):
        if isinstance(value, (list, tuple)):
            value = value[0] + value[1] * 1j
        value = complex(value)
        self.length = abs(value)
        c = self.length
        a = value.real
        b = value.imag
        if b == 0:
            self.angle = Angle(RADIANS, 0)
        elif a == 0:
            self.angle = Angle(DEGREES, 90 * getpan(c))
        else:
            self.angle = Angle(RADIANS, acos(a/c))
    
    def __mul__(self, other):
        other = complex(other)
        return Complex(self.complex)
    
    def __rmul__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) * self.complex)
        else:
            return type(other)(complex(other) * self.complex)
    
    def __divmod__(self, other):
        other = Complex(other)
        return Complex(self.complex / other.complex)
    
    def __rdivmod__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) / self.complex)
        else:
            return type(other)(complex(other) / self.complex)


class Decimal(_Decimal):
    def __init__(self, number):
        super().__new__(self.__class__, float(number))


TWO_WAY = "two-way"
HEAD_TO_TAIL = "head to tail"


class Number:
    def __init__(self, seed, types, l, r, number, fps):
        self.seed = seed
        self.type = types
        self.l = l
        self.r = r
        self.number = number
        self._number = number
        self.direction = 1
        self.fps = fps
        self.start()
    
    def start(self):
        self.started = True
        self.suspended = False
        self.number = self._number
        import threading
        threading.Thread(target=self._update, daemon=True).start()
    
    def suspend(self):
        self.suspended = True
    
    def proceed(self):
        self.suspended = False
    
    def stop(self):
        self.started = False
    
    def _update(self):
        import time
        while self.started:
            while self.suspended:
                pass
            while not self.suspended:
                self.update()
                time.sleep(1 / self.fps)
    
    def getseed(self):
        import random
        if isinstance(self.seed, (int, float)):
            if self.seed <= 0:
                return random.random()
            else:
                return self.seed
        elif isinstance(self.seed, (tuple, list)):
            if isinstance(self.seed[0], random.Random):
                temp = self.seed[0]
                self.seed = self.seed[1:]
            else:
                temp = random
            return temp.uniform(*self.seed)
        elif isinstance(self.seed, random.Random):
            return self.seed.random()
    
    def update(self):
        self.number += self.getseed() * self.direction
        if self.type == TWO_WAY:
            if not l < self._number < self.r:
                self.direction = - self.direction
        elif self.type == HEAD_TO_TAIL:
            if self.number >= self.r:
                self.number += self.l - self.r
        else:
            raise TypeError("type is be '%s' or '%s'" % (TWO_WAY, HEAD_TO_TAIL))
    
    def get(self):
        return self.number
    
    def __get__(self, instance, owner):
        return self.get()
    
    def __float__(self):
        return float(self.get())
    
    def __int__(self):
        return int(self.get())


def getpan(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def ln(x):
    temp = Complex(x)
    if (temp.angle.radians == 0):
        return _math.log(x, e)
    return temp.angle.radians * 1j + ln(temp.length)


def log(x, base=2):
    return ln(x) / ln(base)


def log2(x):
    return log(x)


def lg(x):
    return log(x, 10)


def lim(x):
    return x & (- x)


OPERATOR = {"(": 0, ")": 0, "+": 1, "-": 1, "*": 2, "/": 2, "//": 2, "**": 3, "log": 3}
OPERATOR_FUNC = {"log": log}
for op in OPERATOR.keys():
    if op not in ("(", ")", "log"):
        OPERATOR_FUNC[op] = eval("lambda a, b: a %s b" % op)
reg_d = r"[+-]*\s*(?:\d+(?:\.\d*)?|\.\d*)"
reg_d = r"%s(?:[+-]%s[IJij])?" % (reg_d, reg_d)
reg_exp = r"\s*(%s|(?:\*\*| log )|(?:\*|/{1,2})|[+-]|[()])\s*" % reg_d
_reg_d = _re.compile(reg_d)
SUFFIX = "suffix"
PREFIX = "prefix"
INFIX = "infix"


def isdigit(s):
    if isinstance(s, (float, int, complex, Complex)):
        return True
    return bool(_reg_d.match(s))


def split_exp(exp):
    temp = _re.findall(reg_exp, exp)
    nw = []
    for token in temp:
        if not token:
            continue
        try:
            if token == ".":
                token = 0
            token = Complex(token)
        except:
            pass
        if len(nw) and isdigit(nw[-1]) and isdigit(token):
            nw.append("+")
        nw.append(token)
    return nw


def join_exp(exp):
    return " ".join(map(lambda token: str(token), exp))


def eval_op(op, a, b):
    try:
        op, a, b = str(op), Complex(a), Complex(b)
    except:
        return TypeError("op,a,b parameters must be str,complex,complex")
    return OPERATOR_FUNC[op](a, b)


def reverse_expression(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    nw = []
    for token in reversed(exp):
        if token == "(":
            token = ")"
        elif token == ")":
            token = "("
        nw.append(token)
    return nw


def getSuffix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    stk = _Stk()
    error_turn = TypeError("exp parameter must be a suffix")
    for token in exp:
        if isdigit(token):
            stk.push(token)
        else:
            if len(stk) >= 2:
                stk.push(eval_op(token, stk.pop(), stk.pop()))
            else:
                return error_turn
    if stk.size == 1:
        return stk.top
    else:
        return error_turn


def getPrefix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    stk = _Stk()
    error_turn = TypeError("exp parameter must be a prefix")
    for token in reversed(exp):
        if isdigit(token):
            stk.push(token)
        else:
            try:
                stk.push(eval_op(token, stk.pop(), stk.pop()))
            except:
                return error_turn
    if stk.size > 1:
        return error_turn
    else:
        return stk.top


def Sinfix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    if isinstance(getInfix(exp), Exception):
        return getInfix(exp)
    stk = _Stk()
    nw = []
    i = 0
    mn = 1e18
    for token in exp:
        if token == "(":
            stk.push(i)
            mn = 1e18
        elif token == ")":
            l = stk.pop()
            if l != 0 and mn < OPERATOR[nw[l-1]]:
                i += 2
                nw.insert(l, "(")
                nw.append(")")
            mn = 1e18
            if not stk.empty():
                for tok in nw[stk.top+1:l]:
                    mn = min(mn, OPERATOR[tok])
        else:
            i += 1
            if not isdigit(token):
                mn = min(OPERATOR[token], mn)
            nw.append(token)
            
    return nw


def getInfix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    if exp[0] == "(" and exp[-1] == ")":
        return getInfix(exp[1:-1])
    error_turn = TypeError("exp parameter must be a infix")
    if len(exp) == 1 and not isdigit(exp[0]):
        return error_turn
    mn, mnid = 1e18, -1
    _iter = enumerate(exp)
    for id, token in _iter:
        if token == "(":
            while token != ")":
                id, token = next(_iter)
        if not isdigit(token) and token != ")" and mn >= OPERATOR[token]:
            mn, mnid = OPERATOR[token], id
    if mnid == -1:
        if len(exp) > 1:
            return error_turn
        return exp[0]
    else:
        a = getInfix(exp[:mnid])
        b = getInfix(exp[mnid+1:])
        # print(a, b)
        return eval_op(exp[mnid], a, b)


def getExpressionType(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    for func, typ in zip([getSuffix, getPrefix, getInfix], [SUFFIX, PREFIX, INFIX]):
        temp = func(_cpy(exp))
        if not isinstance(temp, Exception):
            return (typ, func)
    return TypeError("parameter exp must be a expression")


def toSuffix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    et, _ = getExpressionType(exp)
    if isinstance(et, Exception):
        raise et
    if et == PREFIX:
        stk = _Stk()
        for token in reversed(exp):
            if isdigit(token):
                stk.push([token])
            else:
                stk.push([stk.pop(), stk.pop(), token])
        return list(stk)
    elif et == SUFFIX:
        return exp
    else:
        output = []
        stk = _Stk()
        stk.push("(")
        for token in exp + [")"]:
            if isdigit(token):
                output.append(token)
            elif token == "(":
                stk.push(token)
            elif token != ")":
                while not stk.empty() and OPERATOR[stk.top] >= OPERATOR[token]:
                    output.append(stk.pop())
                stk.push(token)
            else:
                while stk.top != "(":
                    output.append(stk.pop())
                stk.pop()
        return output


def toPrefix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    et, _ = getExpressionType(exp)
    if et == INFIX:
        return reverse_expression(toSuffix(reverse_expression(exp)))
    elif et == PREFIX:
        return exp
    else:
        stk = _Stk()
        for token in exp:
            if isdigit(token):
                stk.push([token] + stk.pop() + stk.pop())
            else:
                stk.append([token])
        return stk.top


def toInfix(exp):
    if isinstance(exp, str):
        exp = split_exp(exp)
    exp = toSuffix(exp)
    stk = _Stk()
    for token in exp:
        if isdigit(token):
            stk.push([token])
        else:
            b = stk.pop()
            a = stk.pop()
            stk.push(["(", *a, token, *b, ")"])
    return stk.top


class Expression(_BTree):
    @_overload
    def __init__(self, point, left, right):
        super(Expression, self).__init__(point)
        if not isinstance(left, self.__class__):
            left = self.__class__(left)
        if not isinstance(right, self.__class__):
            right = self.__class__(right)
        self.left = left
        self.right = right
    
    @_overload
    def __init__(self, __obj):
        if not isinstance(__obj, _BTree):
            raise TypeError("__obj parameter must be BinaryTree")
        super(Expression, self).__init__(_cpy(__obj.head))
        self.left = __obj.left.copy()
        self.right = __obj.right.copy()
    
    def copy(self):
        if self.left is not None:
            nw = Expression(_cpy(self.head), self.left.copy(), self.right.copy())
        else:
            nw = Expression(_cpy(self.head))
        return nw
    
    @_overload
    def __init__(self, exp):
        if isinstance(exp, Complex):
            super(Expression, self).__init__(Complex(exp))
            return
        exp = toSuffix(exp)
        super(Expression, self).__init__(exp)
        stk = _Stk()
        for token in exp:
            if isinstance(token, Complex):
                stk.push(Expression(token))
            else:
                b, a = stk.pop(), stk.pop()
                stk.push(Expression(token, a, b))
        self.__init__(stk.top)
        
    def __repr__(self):
        return str(join_exp(self.getExpression((INFIX))))
    
    def inorder(self):
        turn = ()
        left = self.left
        if left:
            turn += ("(", *left.inorder(), ")")
        turn += (self.head,)
        right = self.right
        if right:
            turn += ("(", *right.inorder(), ")")
        return turn
    
    def getExpression(self, typ):
        match typ:
            case "infix":
                return self.inorder()
            case "suffix":
                return self.postorder()
            case "prefix":
                return self.preorder()
            case UnkownType:
                raise TypeError("typ parameter most be infix, suffix or prefix, not %s" % UnkownType)


if __name__ == "__main__":
    _exp = "1.5+1i + 2 ** (4.+2)"
    print(_exp)
    print(getInfix(_exp))
    print(join_exp(toPrefix(_exp)))
    print(join_exp(toSuffix(_exp)))
    temp = toInfix(toSuffix(_exp))
    print(join_exp(temp))
    print(join_exp(Sinfix(temp)))
    print()
    _exptree = Expression(_exp)
    for typ in [INFIX, SUFFIX, PREFIX]:
        print(_exptree.getExpression(typ))
