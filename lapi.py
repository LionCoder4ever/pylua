from enum import Enum

luatypelist = [(j, i) for i, j in enumerate(['LUA_TNONE', 'LUA_TNIL', 'LUA_TBOOLEAN', 'LUA_TLIGHTUSERDATA',
                                             'LUA_TNUMBER', 'LUA_TSTRING', 'LUA_TTABLE', 'LUA_TFUNCTION',
                                             'LUA_TUSERDATA', 'LUA_TTHREAD'])]

LUATYPE = Enum('LUATYPE', luatypelist)


class LuaValue:
    def __init__(self, *args):
        self.type, self.value = args

    def typeOf(self):
        typeInPy = type(self.value)
        if typeInPy is type(None):
            return LUATYPE.LUA_TNIL.value
        elif typeInPy is bool:
            return LUATYPE.LUA_TBOOLEAN.value
        elif typeInPy is int:
            return LUATYPE.LUA_TNUMBER.value
        elif typeInPy is float:
            return LUATYPE.LUA_TNUBER.value
        elif typeInPy is str:
            return LUATYPE.LUA_TSTRING.value
        else:
            raise TypeError('UNKONW type')

    def __str__(self):
        return self.value


class LuaStack:
    def __init__(self, size):
        self.slots = []
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
            raise RuntimeError('stack overflow')
        self.slots[self.top] = luaValue
        self.top += 1

    def pop(self):
        if self.top < 1:
            raise RuntimeError('stack underflow')
        self.top -= 1
        item = self.slots.pop(self.top)
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


class LuaState:
    def __init__(self):
        self.stack = newLuaStack(20)

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
        self.stack.push(LuaValue(LUATYPE.LUA_TNUMBER.value, number))

    def PushNumber(self, number):
        self.stack.push(LuaValue(LUATYPE.LUA_TNUMBER.value, number))

    def PushString(self, str):
        self.stack.push(LuaValue(LUATYPE.LUA_TSTRING.value, str))

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

    def ISNoneOrNil(self, index):
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
        value = self.stack.get(index).value
        valueType = type(value)
        if valueType is int:
            return value, True
        elif valueType is float:
            return float(value), True
        else:
            return 0, False

    def ToInteger(self,index):
        return self.ToIntegerX(index)[0]

    def ToIntegerX(self,index):
        return int(self.stack.get(index).value),type(self.stack.get(index).value) is int

    def ToStringX(self,index):
        value = self.stack.get(index).value
        valueType = type(value)
        if valueType is str:
            return value,True
        elif valueType is int or valueType is float:
            toStrValue = str(value)
            self.stack.set(index,toStrValue)
            return toStrValue,True
        else:
            return "",False

    def ToString(self,index):
        return self.ToStringX(index)[0]
