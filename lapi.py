from math import pow
from typing import List

from lmath import ShiftLeft, ShiftRight
from lop import Instruction, OPCODE, COMOPENUM, ARIOPENUM
from ltable import LuaArray, LuaTable
from lvalue import LuaNil, LuaValue, LuaString, LuaNumber, LUATYPE, LuaClosure
from lvm import LuaVM

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


class LuaStack:
    def __init__(self, size: int, ls):
        self.slots = LuaArray()
        self.size = size
        self.top = 0
        for i in range(size):
            self.slots.append(LuaNil())
        self.prev = None
        self.closure = None
        self.varargs = None
        self.pc = 0
        self.ls = ls

    def check(self, n):
        free = len(self.slots) - self.top
        # if free < n:
        for i in range(free, n):
            self.slots.append(LuaNil())

    def push(self, luaValue):
        if self.top == len(self.slots):
            # self.check(n)
            raise RuntimeError('stack overflow')
        self.slots[self.top] = luaValue
        self.top += 1

    def pushN(self, values: List[LuaValue], n: int):
        # if values is  None:
        #     return
        valuesNum = len(values)
        if n < 0:
            n = valuesNum
        for i in range(n):
            if i < valuesNum:
                self.push(values[i])
            else:
                self.push(LuaNil())

    def pop(self) -> LuaValue:
        if self.top < 1:
            raise RuntimeError('stack underflow')
        self.top -= 1
        # replace pop slots with set the slot to lua nil
        item = self.slots[self.top]
        self.slots[self.top] = LuaNil()
        return item

    def popN(self, n: int) -> List[LuaValue]:
        tmplist = [LuaNil()] * n
        for i in range(n - 1, -1, -1):
            tmplist[i] = self.pop()
        return tmplist

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


def newLuaStack(size,ls):
    return LuaStack(size,ls)


class LuaState(LuaVM):
    LUA_MINSTACK = 20
    LUA_MAXSTACK = 1000000
    LUA_REGISTRYINDEX = -LUA_MAXSTACK - 1000
    LUA_RIDX_GLOBALS = 2

    def __init__(self):
        self.stack = newLuaStack(self.LUA_MINSTACK,self)
        self.registry = LuaTable(0, 0)
        self.registry.put(LuaNumber(self.LUA_RIDX_GLOBALS), LuaTable(0, 0))
        self.pushLuaStack(newLuaStack(self.LUA_MINSTACK,self))

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
                self.stack.push(LuaNil())

    def PushNil(self):
        self.stack.push(LuaNil())

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

    def Len(self, index: int):
        item = self.stack.get(index)
        if item.type is LUATYPE.LUA_TSTRING.value:
            self.stack.push(LuaNumber(len(item.value)))
        elif item.type is LUATYPE.LUA_TTABLE.value:
            self.stack.push(LuaNumber(item.value.len()))
        else:
            raise TypeError('# operator get error parameter')

    def Concat(self, num: int):
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
        t = self.stack.get(index)
        k = self.stack.pop()
        return self.getTable(t, k)

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

    def pushLuaStack(self, stack: LuaStack):
        stack.prev = self.stack
        self.stack = stack

    def popLuaStack(self):
        stack = self.stack
        self.stack = stack.prev
        stack.prev = None

    def Load(self, chunk, chunkName: str, mode: str):
        from readChunk import HandleFile
        handleFile = HandleFile(chunk)
        handleFile.readHead()
        proto = handleFile.readProtos(0)
        self.stack.push(LuaClosure(proto))
        return 0

    def Call(self, nArgs: int, nResults: int):
        closure = self.stack.get(-(nArgs + 1))
        if isinstance(closure, LuaClosure):
            if closure.value is not None:
                print("call {}<{},{}>".format(closure.value.source, closure.value.lineDef, closure.value.lastLineDef))
                self.callLuaClosure(nArgs, nResults, closure)
            else:
                self.callPyClosure(nArgs, nResults, closure)
        else:
            raise TypeError('call element is not function')

    def callLuaClosure(self, nArgs: int, nResults: int, closure: LuaClosure):
        nRegs = closure.value.maxStackSize
        nParams = closure.value.numParms
        newStack = LuaStack(nRegs + 20)
        newStack.closure = closure
        funcAndArgs = self.stack.popN(nArgs + 1)
        newStack.pushN(funcAndArgs[1:], nParams)
        newStack.top = nRegs
        if nArgs > nParams and closure.value.isVararg:
            newStack.varargs = funcAndArgs[nParams + 1:]
        self.pushLuaStack(newStack)
        self.runLuaClosure()
        self.popLuaStack()

    def callPyClosure(self, nArgs: int, nResults: int, closure: LuaClosure):
        newStack = LuaStack(nArgs + 20)
        newStack.closure = closure
        args = self.stack.popN(nArgs)
        newStack.pushN(args, nArgs)
        self.stack.pop()
        self.pushLuaStack(newStack)
        result = closure.pyFunc()
        self.popLuaStack()
        if nResults is not 0:
            results = newStack.popN(result)
            self.stack.check(len(results))
            self.stack.pushN(results, nResults)

    def PushPyFunction(self, func):
        self.stack.push(LuaClosure(None, func))

    def IsPyFunction(self, index: int):
        value = self.stack.get(index)
        if isinstance(value, LuaClosure):
            return value.pyFunc is not None
        return False

    def ToPyFunction(self, index: int):
        value = self.stack.get(index)
        if isinstance(value, LuaClosure):
            return value.pyFunc
        return None

    def runLuaClosure(self):
        while True:
            inst = Instruction(self.Fetch())
            inst.execute(self)
            if inst.getOpcode() is OPCODE.OP_RETURN.value:
                break
