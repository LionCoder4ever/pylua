import collections
from enum import Enum
from lmath import FloatToInteger, ShiftLeft, ShiftRight
from math import pow

luatypelist = [(j, i) for i, j in enumerate(['LUA_TNONE', 'LUA_TNIL', 'LUA_TBOOLEAN', 'LUA_TLIGHTUSERDATA',
                                             'LUA_TNUMBER', 'LUA_TSTRING', 'LUA_TTABLE', 'LUA_TFUNCTION',
                                             'LUA_TUSERDATA', 'LUA_TTHREAD'])]

LUATYPE = Enum('LUATYPE', luatypelist)
arithoplist = [(j, i) for i, j in enumerate(['LUA_OPADD', 'LUA_OPSUB', 'LUA_OPMUL', 'LUA_OPMOD', 'LUA_OPPOW',
                                             'LUA_OPDIV', 'LUA_OPIDI', 'LUA_OPBAN', 'LUA_OPBOR', 'LUA_OPBXO',
                                             'LUA_OPSHL', 'LUA_OPSHR', 'LUA_OPUNM', 'LUA_OPBNOT'])]
ARIOPENUM = Enum('ARIOP', arithoplist)

compareoplist = [(j, i) for i, j in enumerate(['LUA_OPEQ', 'LUA_OPLT', 'LUA_OPLE'])]
COMOPENUM = Enum('COMOP', compareoplist)

iadd = fadd = lambda a, b: a + b
isub = fsub = lambda a, b: a - b
imul = fmul = lambda a, b: a * b
imod = fmod = lambda a, b: a % b
lpow = pow
div = lambda a, b: a / b
iidiv = fidiv = lambda a, b: a // b
band = lambda a, b: a & b
bor = lambda a, b: a | b
bxor = lambda a, b: a ^ b
shl = ShiftLeft
shr = ShiftRight
iunm = funm = lambda a: -a
bnot = lambda a: ~a

arithOperators = [(iadd, fadd), (isub, fsub), (imul, fmul), (imod, fmod), (None, lpow), (None, div), (iidiv, fidiv),
                  (band, None), (bor, None), (bxor, None), (shl, None), (shr, None), (iunm, funm), (bnot, None)]


class LuaValue:
    def __init__(self, *args):
        self.type, self.value = args

    def typeOf(self):
        return self.type

    def convertToFloat(self):
        typeOfValue = type(self.value)
        if typeOfValue is float:
            return self.value, True
        elif typeOfValue is int or typeOfValue is str:
            return float(self.value), True
        else:
            return 0, False

    def convertToInteger(self):
        typeOfValue = type(self.value)
        if typeOfValue is int:
            return self.value, True
        elif typeOfValue is float:
            return FloatToInteger(self.value)
        elif typeOfValue is str:
            try:
                return int(self.value), True
            except ValueError:
                return FloatToInteger(float(self.value))
        else:
            return 0, False

    @staticmethod
    def arith(a, b, op):
        if op[1] is None:
            if a is not None:
                x, aok = a.convertToInteger()
                if aok:
                    y, bok = b.convertToInteger()
                    if bok:
                        return LuaNumber(op[0](x, y))
            else:
                y, bok = b.convertToInteger()
                if bok:
                    return LuaNumber(op[0](y))
        else:
            if op[0] is not None:
                try:
                    return LuaNumber(op[0](int(a.value), int(b.value)))
                except ValueError:
                    pass
            x, aok = a.convertToFloat()
            if aok:
                y, bok = b.convertToFloat()
                if bok:
                    return LuaNumber(op[1](x, y))
        return LuaValue(LUATYPE.LUA_TNIL.value, None)

    @staticmethod
    def eq(a, b) -> bool:
        if a.type != b.type:
            return False
        avalue = a.value
        atype = type(avalue)
        bvalue = b.value
        btype = type(bvalue)
        if avalue is None:
            return bvalue is None
        elif atype is bool:
            return bool(bvalue) == avalue
        elif atype is str:
            return str(bvalue) == avalue
        elif atype is int or atype is float:
            if btype is int or btype is float:
                return avalue == bvalue
            else:
                return False
        else:
            return a == b

    @staticmethod
    def lt(a, b):
        avalue = a.value
        atype = type(avalue)
        bvalue = b.value
        btype = type(bvalue)
        if atype is str:
            return avalue < str(bvalue)
        elif atype is int or atype is float:
            if btype is int or btype is float:
                return avalue < bvalue
            else:
                raise TypeError('error comparison parameter')
        else:
            raise TypeError('error comparison')

    @staticmethod
    def le(a, b):
        """
        le: less than or equal to
        -.-!
        :param a: LuaValue
        :param b: LuaValue
        :return:
        """
        avalue = a.value
        atype = type(avalue)
        bvalue = b.value
        btype = type(bvalue)
        if atype is str:
            return avalue <= str(bvalue)
        elif atype is int or atype is float:
            if btype is int or btype is float:
                return avalue <= bvalue
            else:
                raise TypeError('error comparison parameter')
        else:
            raise TypeError('error comparison')

    def __str__(self):
        return self.value


class LuaNumber(LuaValue):
    def __init__(self, value: int or float):
        super().__init__(LUATYPE.LUA_TNUMBER.value, value)

    def __repr__(self):
        return self.value


class LuaString(LuaValue):
    def __init__(self, value: str):
        super().__init__(LUATYPE.LUA_TSTRING.value, value)

    def __repr__(self):
        return self.value


class LuaStack:
    def __init__(self, size):
        self.slots = LuaArray()
        self.size = size
        self.top = 0
        for i in range(size):
            self.slots.append(LuaValue(LUATYPE.LUA_TNIL.value, None))

    def check(self, n):
        free = len(self.slots) - self.top
        if free < n:
            for i in range(n - free):
                self.slots.append(LuaValue(LUATYPE.LUA_TNIL.value, None))

    def push(self, luaValue):
        if self.top == len(self.slots):
            # self.check(n)
            raise RuntimeError('stack overflow')
        self.slots[self.top] = luaValue
        self.top += 1

    def pop(self) -> LuaValue:
        if self.top < 1:
            raise RuntimeError('stack underflow')
        self.top -= 1
        # replace pop slots with set the slot to lua nil
        item = self.slots[self.top]
        self.slots[self.top] = LuaValue(LUATYPE.LUA_TNIL.value, None)
        return item

    def absIndex(self, index):
        return index if index >= 0 else index + self.top + 1

    def isValid(self, index):
        absIndex = self.absIndex(index)
        return absIndex and 0 < absIndex <= self.top

    def get(self, index):
        absIndex = self.absIndex(index)
        if 0 < absIndex <= self.top:
            item = self.slots[absIndex - 1]
            return item
        return None

    def set(self, index, luavalue):
        absIndex = self.absIndex(index)
        if 0 < absIndex <= self.top:
            self.slots[absIndex - 1] = luavalue
            return
        raise IndexError('invalid index')

    def reverse(self, fromindex, toindex):
        # slots = self.slots
        while fromindex < toindex:
            self.slots[fromindex], self.slots[toindex] = self.slots[toindex], self.slots[fromindex]
            fromindex += 1
            toindex -= 1


def newLuaStack(size):
    return LuaStack(size)


class LuaDict(collections.Mapping):
    def __init__(self):
        self.map = {}

    def __setitem__(self, key, value):
        if not isinstance(key, LuaValue):
            raise TypeError('key must be instance of LuaValue')
        if not isinstance(value, LuaValue):
            raise TypeError('value must be instance of  LuaValue')
        self.map[key] = value

    def __getitem__(self, item):
        return self.map.get(item)

    def __iter__(self):
        return iter(self.map)

    def __len__(self):
        return len(self.map)


class LuaArray(collections.MutableSequence):
    def __init__(self):
        self.arr = []

    def __delitem__(self, key):
        del self.arr[key]

    def __getitem__(self, item):
        return self.arr[item]

    def __len__(self):
        return len(self.arr)

    def __setitem__(self, key, value):
        LuaArray.assertValue(value)
        self.arr[key] = value

    def insert(self, index, value):
        LuaArray.assertValue(value)
        self.arr.insert(index, value)

    @staticmethod
    def assertValue(value):
        if not isinstance(value, LuaValue):
            raise TypeError('value must be instance of  LuaValue')


class LuaTable(LuaValue):
    LFIELDS_PER_FLUSH = 50

    def __init__(self, narr: int, nrec: int):
        super().__init__(LUATYPE.LUA_TTABLE.value, self)
        if narr > 0:
            self.arr = LuaArray()
        if nrec > 0:
            self.map = LuaDict()

    def get(self, key: LuaValue) -> LuaValue:
        """
        if key is int or can be convert to int,get value from array
        :param key:
        :return:
        """
        key = self.floatToInteger(key)
        if type(key.value) is int and (1 <= key.value <= len(self.arr)):
            return self.arr[key.value - 1]
        return self.map.get(key)

    def put(self, key, value):
        key = self.floatToInteger(key)
        if type(key.value) is int and key.value >= 1:
            if key.value <= len(self.arr):
                self.arr[key.value - 1] = value
                if key.value == len(self.arr) and value.value is None:
                    self.shrinkArray()
                return
            if key.value == len(self.arr) + 1:
                if hasattr(self, 'map'):
                    del self.map[key]
                if value.value is not None:
                    self.arr.append(value)
                    self.expandArray()
                return
        if value.value is not None:
            if not hasattr(self, 'map'):
                self.map = LuaDict()
            self.map[key] = value
        else:
            del self.map[key]

    def floatToInteger(self, key):
        """
        if key is float,try convert to int
        :param key:
        :return:
        """
        if key.typeOf() is LUATYPE.LUA_TNUMBER.value:
            if type(key.value) is float:
                keytoint, convert = FloatToInteger(key.value)
                if convert:
                    key.value = keytoint
                    return key
        return key

    def shrinkArray(self):
        for i in range(1, len(self.arr) + 1):
            if self.arr[-i].value is None:
                self.arr.pop()
            else:
                break

    def expandArray(self):
        """
        move item in map to arr
        :return:
        """
        idx = len(self.arr) + 1
        if hasattr(self, 'map'):
            for i in self.map.keys():
                if int(i.value) is idx:
                    self.arr.append(self.map[i])
                    del self.map[i]
                    idx += 1
                else:
                    break

    def len(self) -> int:
        return len(self.arr)


class LuaState:
    def __init__(self, proto=None):
        self.stack = newLuaStack(20)
        self.proto = proto
        self.pc = 0

    def GetTop(self):
        return self.stack.top

    def AbsIndex(self, index):
        return self.stack.absIndex(index)

    def CheckStack(self, n):
        self.stack.check(n)
        return True

    def Pop(self, n):
        # for i in range(n):
        #     self.stack.pop()
        self.SetTop(-n - 1)

    def Copy(self, fromIndex, toIndex):
        self.stack.set(toIndex, self.stack.get(fromIndex))

    def PushValue(self, index):
        self.stack.push(self.stack.get(index))

    def Replace(self, index):
        item = self.stack.pop()
        self.stack.set(index, item)

    def Insert(self, index):
        self.Rotate(index, 1)

    def Remove(self, index):
        self.Rotate(index, -1)
        self.Pop(1)

    def Rotate(self, index, n):
        t = self.stack.top - 1
        p = self.stack.absIndex(index) - 1
        m = t - n if n >= 0 else p - n - 1
        self.stack.reverse(p, m)
        self.stack.reverse(m + 1, t)
        self.stack.reverse(p, t)

    def SetTop(self, index):
        newTop = self.stack.absIndex(index)
        if newTop < 0:
            raise RuntimeError('stack underflow')
        n = self.stack.top - newTop
        if n > 0:
            for i in range(n):
                self.stack.pop()
        elif n < 0:
            for i in range(abs(n)):
                self.stack.push(LuaValue(LUATYPE.LUA_TNIL.value, None))

    def PushNil(self):
        self.stack.push(LuaValue(LUATYPE.LUA_TNIL.value, None))

    def PushBoolean(self, bool):
        self.stack.push(LuaValue(LUATYPE.LUA_TBOOLEAN.value, bool))

    def PushInteger(self, number):
        self.stack.push(LuaNumber(number))

    def PushNumber(self, number):
        self.stack.push(LuaNumber(number))

    def PushString(self, str):
        self.stack.push(LuaString(str))

    def TypeName(self, tp):
        if tp is LUATYPE.LUA_TNONE.value:
            return "no value"
        elif tp is LUATYPE.LUA_TNIL.value:
            return "nil"
        elif tp is LUATYPE.LUA_TBOOLEAN.value:
            return "bool"
        elif tp is LUATYPE.LUA_TNUMBER.value:
            return "number"
        elif tp is LUATYPE.LUA_TSTRING.value:
            return "string"
        elif tp is LUATYPE.LUA_TTABLE.value:
            return "table"
        elif tp is LUATYPE.LUA_TFUNCTION.value:
            return "function"
        elif tp is LUATYPE.LUA_TTHREAD.value:
            return "thread"
        else:
            return "userdata"

    def Type(self, index):
        if self.stack.isValid(index):
            return self.stack.get(index).typeOf()
        return LUATYPE.LUA_TNONE.value

    def IsNone(self, index):
        return self.Type(index) == LUATYPE.LUA_TNONE.value

    def IsNil(self, index):
        return self.Type(index) == LUATYPE.LUA_TNIL.value

    def IsNoneOrNil(self, index):
        return self.Type(index) <= LUATYPE.LUA_TNIL.value

    def IsBoolean(self, index):
        return self.Type(index) == LUATYPE.LUA_TBOOLEAN.value

    def IsString(self, index):
        type = self.Type(index)
        return type == LUATYPE.LUA_TSTRING.value or type == LUATYPE.LUA_TNUMBER.value

    def IsNumber(self, index):
        return self.ToNumberX(index)[1]

    def IsInteger(self, index):
        return type(self.stack.get(index).value) is int

    def ToBoolean(self, index):
        return bool(self.stack.get(index).value)

    def ToNumber(self, index):
        return self.ToNumberX(index)[0]

    def ToNumberX(self, index):
        luavalue = self.stack.get(index)
        return luavalue.convertToFloat()

    def ToInteger(self, index):
        return self.ToIntegerX(index)[0]

    def ToIntegerX(self, index):
        return self.stack.get(index).convertToInteger()

    def ToStringX(self, index):
        value = self.stack.get(index).value
        valueType = type(value)
        if valueType is str:
            return LuaString(value), True
        elif valueType is int or valueType is float:
            toStrValue = LuaString(str(value))
            self.stack.set(index, toStrValue)
            return toStrValue, True
        else:
            return "", False

    def ToString(self, index):
        return self.ToStringX(index)[0]

    def Arith(self, op):
        a = None
        b = self.stack.pop()
        if op != ARIOPENUM.LUA_OPUNM.value and op != ARIOPENUM.LUA_OPBNOT.value:
            a = self.stack.pop()
        operator = arithOperators[op]
        result = LuaValue.arith(a, b, operator)
        if result is not None:
            self.stack.push(result)
        else:
            raise ArithmeticError('arithmetic error')

    def Compare(self, idx1, idx2, compareOp):
        a = self.stack.get(idx1)
        b = self.stack.get(idx2)
        if compareOp == COMOPENUM.LUA_OPEQ.value:
            return LuaValue.eq(a, b)
        elif compareOp == COMOPENUM.LUA_OPLT.value:
            return LuaValue.lt(a, b)
        elif compareOp == COMOPENUM.LUA_OPLE.value:
            return LuaValue.le(a, b)
        else:
            raise RuntimeError('invalid compare operation')

    def Len(self, index):
        item = self.stack.get(index)
        if item.type is LUATYPE.LUA_TSTRING.value:
            self.stack.push(LuaNumber(len(item.value)))
        elif item.type is LUATYPE.LUA_TTABLE.value:
            self.stack.push(LuaNumber(item.value.len()))
        else:
            raise TypeError('# operator get error parameter')

    def Concat(self, num):
        if num == 0:
            self.stack.push('')
        elif num >= 2:
            for i in range(1, num):
                if self.IsString(-1) and self.IsString(-2):
                    s2 = self.ToString(-1)
                    s1 = self.ToString(-2)
                    self.stack.pop()
                    self.stack.pop()
                    self.stack.push(LuaString(s1.value + s2.value))
                else:
                    raise TypeError('... operation error')

    def CreateTable(self, narr: int, nrec: int):
        self.stack.push(LuaTable(narr, nrec))

    def NewTable(self):
        self.CreateTable(0, 0)

    def getTable(self, t: LuaTable, key: LuaValue) -> LuaValue:
        if t.type is not LUATYPE.LUA_TTABLE.value:
            raise TypeError('get value from a element not a table')
        value = t.get(key)
        self.stack.push(value)
        return value.typeOf()

    def GetTable(self, index: int) -> LuaValue:
        return self.getTable(self.stack.get(index), self.stack.pop())

    def GetField(self, index: int, key: LuaString):
        return self.getTable(self.stack.get(index), key)

    def GetI(self, index: int, key: LuaNumber):
        return self.getTable(self.stack.get(index), key)

    def SetTable(self, index: int):
        t = self.stack.get(index)
        value = self.stack.pop()
        key = self.stack.pop()
        self.setTable(t, key, value)

    def setTable(self, t: LuaTable, key: LuaValue, value: LuaValue):
        if t.type is not LUATYPE.LUA_TTABLE.value:
            raise TypeError('set value to a element not a table')
        t.put(key, value)

    def SetField(self, index: int, key: LuaString):
        self.setTable(self.stack.get(index), key, self.stack.pop())

    def SetI(self, index: int, key: int):
        self.setTable(self.stack.get(index), LuaNumber(key), self.stack.pop())
