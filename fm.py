import math as _math
from decimal import Decimal as _Decimal
from math import *
from pyns.func import lhas as _lhas, overload as _overload, rhas as _rhas
from pyns.structures import HashList as _HashList


def isEvenNumber(x):
    return x % 2 == 0


def isOddNumber(x):
    return x % 2 != 0


def pow(x, _exp=2):
    return _math.pow(x, _exp)


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
    for i in range(102, int(sqrt(x))):
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
                prime.append(i)
            for j in range(i * 2, x+1, i):
                is_Prime[j] = False
        elif i not in composite:
            composite.append(i)
    return is_Prime


update_prime(1000)

isEven = even = isEvenNumber
isOdd  = odd  = isOddNumber
Hong = "宏"
Gou  = "勾"
Gu   = "股"


class Edge:
    def __getattribute__(self, item):
        if item == "value":
            return super(Horn, self).__getattribute__(item)
        else:
            return self.value.__getattribute__(item)
    
    def __init__(self, value):
        self.value = int(value)
    
    def __int__(self):
        return self.value


class Triangle:
    @_overload
    def __init__(self, *egdes):
        egdes = list(egdes)
        if len(egdes) == 2:
            egdes.append(Hong)
        elif len(egdes) != 3:
            raise ValueError
        if isinstance(egdes[-1], (str, tuple, list)):
            if egdes[-1] == Hong or Hong not in egdes[-1]:
                egdes[-1] = sqrt(pow(egdes[0], 2) + pow(egdes[1], 2))
            else:
                indexHong = egdes[-1].index(Hong)
                egdes[-1] = sqrt(pow(egdes[indexHong], 2) - pow(egdes[indexHong ^ 1], 2))
            
        self.egdes = egdes
        self.horns = (None, None, None) # 计算角度 Horn

    @_overload
    def __init__(self, edge, horn1, horn2, horn3):
        self.horns = horns
        self.egdes = (None, None, None) # 计算边长 Edge
    
    @staticmethod
    def givenTheTwoCornersAndOneSideSeeksTheOtherSide(side, corner1, corner2):
        return side / corner1 * corner2


givenTheTwoCornersAndOneSideSeeksTheOtherSide = \
    Triangle.givenTheTwoCornersAndOneSideSeeksTheOtherSide


def isint(x, ar=1e-6):
    return abs(x - round(x)) <= ar


def toint(x, ar=1e-6):
    if isint(x, ar):
        return int(x)
    else:
        return x


def tointfloat(x, accuracy=1000):
    x *= accuracy
    return toint(x) / accuracy


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
            if temp[i] == "0":
                if ret == "" or  ret[-1] != n[0]:
                    ret += n[0]
            else:
                ret += n[int(temp[i])]
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
        else:
            self.degrees = degrees(number)
    
    @property
    def degrees(self):
        return self._degrees
    
    @degrees.setter
    def degrees(self, value):
        if isint(value):
            self._degrees = float(round(value))
        else:
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
    
    def __str__(self):
        return "%.2f°" % (int(self) if isint(self.degrees) else float(self))
    
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


epowi = e ** 1j


@_overload
def numbers(start, number, step=1):
    return range(start, number * step + start, step)


@_overload
def numbers(number):
    return range(number)


def epow(_exp, powi=False):
    if powi:
        return epowi ** _exp
    else:
        return pow(e, _exp)


IMAG = "imag"
REAL = "real"


def tocomplexint(x):
    if x.imag == 0:
        return tointfloat(x.real)
    for toget in (IMAG, REAL):
        temp = getattr(x, toget)
        if isint(temp):
            x += (round(temp) - temp) * (1j if toget == IMAG else 1)
    return x


def tocomplexintfloat(x, accuracy=1000):
    return tocomplexint(x * accuracy) / accuracy


class Complex:
    def __add__(self, other):
        other = Complex(other)
        return Complex(self.complex + other.complex)
    
    def __radd__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) + self.complex)
        else:
            return type(other)(complex(other) + self.complex)
    
    def __sub__(self, other):
        other = Complex(other)
        return Complex(self.complex - other.complex)
    
    def __rsub__(self, other):
        if isinstance(other, (int, float, complex)):
            return complex(complex(other) - self.complex)
        else:
            return type(other)(complex(other) - self.complex)
    
    def epow(self):
        return Complex(e ** self)
    
    def epowi(self):
        return Complex(epowi ** self)

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
        return self.complex
    
    @_overload
    def __init__(self, __obj):
        if isinstance(__obj, (complex, str, int, float)):
            self.complex = __obj
        elif isinstance(__obj, (list, tuple)):
            self.__init__(*__obj)
        else:
            raise TypeError("__obj must be comlex, str, int, float, list or tuple")
        
    @_overload
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length
    
    @_overload
    def __init__(self, types, number, length):
        self.__init__((types, number), length)
    
    def __repr__(self):
        return "%s object: \n\tangle: %s, \n\tlength:%s, \n= %s" % (
            self.__class__.__name__,
            self.angle,
            self.length,
            self.complex,
        )
    
    def __str__(self):
        return str(self.complex)
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        if isinstance(value, Angle):
            if isinstance(value.radians, (complex, Complex)):
                r = value.radians
                r = complex(r)
                length = e ** - r.imag
                self.length *= length
                value.radians = r.real
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
        return tointfloat(self.complex.imag)
    
    @imag.setter
    def imag(self, value):
        if isinstance(value, (complex, Complex)):
            imag = value.real
            real = - value.imag
            imag = tointfloat(imag)
            real = tointfloat(real)
            self.complex = (real, imag)
            return
        value = tointfloat(value)
        self.complex = (self.real, value)
    
    @property
    def real(self):
        return tointfloat(self.complex.real)
    
    @real.setter
    def real(self, value):
        if isinstance(value, (complex, Complex)):
            self.complex = (tointfloat(value.real), tointfloat(self.imag + value.imag))
        value = tointfloat(value)
        self.complex = (value, self.imag)
    
    @property
    def complex(self):
        return tocomplexintfloat(self.length * epow(self.angle.radians, True))
    
    @complex.setter
    def complex(self, value):
        if isinstance(value, (list, tuple)):
            value = value[0] + value[1] * 1j
        value = complex(value)
        self.length = tointfloat(abs(value))
        a = self.length
        b = value.real
        c = value.imag
        if a == 0:
            self.angle = Angle(RADIANS, 0)
        elif b == 0:
            self.angle = Angle(DEGREES, 90 * getpan(c))
        else:
            self.angle = Angle(RADIANS, acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))
    
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
        super().__new__(self.__class__, tointfloat(float(number)))


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
    return temp.angle.radians * 1j + loge(temp.length)


def log(x, base=2):
    return ln(x) / ln(base)


def log2(x):
    return log(x)


def lg(x):
    return log(x, 10)


def lim(x):
    return x & (- x)
