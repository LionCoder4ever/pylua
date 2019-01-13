from lapi import ARIOPENUM
from readChunk import Instruction


class LuaVM:
    def __init__(self, l):
        self.ls = l

    def PC(self) -> int:
        return self.ls.pc

    def AddPC(self, n):
        self.ls.pc += n

    def Fetch(self) -> int:
        op = self.ls.proto.code[self.ls.pc]
        self.ls.pc += 1
        return op

    def GetConst(self, index):
        cons = self.ls.proto.constants[index]
        self.ls.stack.push(cons)

    # put const value or stack value
    def GetRk(self, rk):
        if rk > 0xFF:
            self.GetConst(rk & 0xFF)
        else:
            self.ls.PushValue(rk + 1)


def move(i, vm):
    """
    R（A）：=R（B）
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, _ = i.getAbc()
    a += 1
    b += 1
    vm.ls.Copy(b, a)


def jmp(i, vm):
    a, sBx = i.getAsbx()
    vm.AddPC(sBx)
    if a != 0:
        # TODO add upvalue support
        raise RuntimeError('reference to upvalue')


def loadNil(i, vm):
    """
    R(A), R(A+1), ..., R(A+B) := nil
    push nil to the top of stack
    copy (a+b) times then remove the first nil
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, _ = i.getAbc()
    a += 1
    vm.ls.PushNil()
    for i in range(a, a + b + 1):
        vm.ls.Copy(-1, i)
    vm.ls.Pop(1)


def loadBool(i, vm):
    """
    R(A) := (bool)B; if (C) pc++
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, c = i.getAbc()
    a += 1
    vm.ls.PushBoolean(b != 0)
    vm.ls.Replace(a)
    if c != 0:
        vm.AddPC(1)


def loadK(i, vm):
    """

    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, bx = i.getAbx()
    a += 1
    vm.ls.GetConst(bx)
    vm.ls.Replace(a)


def loadKx(i, vm):
    """
    add EXTRAARG op
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, _ = i.getAbx()
    a += 1
    ax = Instruction(vm.Fetch()).getAx()
    vm.ls.GetConst(ax)
    vm.ls.Replace(a)


def binaryrith(i, vm, op):
    """
    R(A) := RK(B) op RK(C)
    :param i: Instruction
    :param vm: LuaVM
    :param op: ArithOp
    :return:
    """
    a, b, c = i.getAbc()
    a += 1
    vm.GetRk(b)
    vm.GetRk(c)
    vm.ls.Arith(op)
    vm.ls.Replace(a)


def unaryArith(i, vm, op):
    """
    R(A) := op R(B)
    :param i: Instruction
    :param vm: LuaVM
    :param op: ArithOp
    :return:
    """
    a, b, _ = i.getAbc()
    a += 1
    b += 1
    vm.ls.PushValue(b)
    vm.ls.Arith(op)
    vm.ls.Replace(a)


add = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPADD.value)
sub = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPSUB.value)
mul = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPMUL.value)
mod = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPMOD.value)
lpow = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPPOW.value)
div = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPDIV.value)
idiv = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPIDIV.value)
band = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPBAND.value)
bor = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPBOR.value)
bxor = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPBXOR.value)
shl = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPSHL.value)
shr = lambda i, vm: binaryrith(i, vm, ARIOPENUM.LUA_OPSHR.value)
unm = lambda i, vm: unaryArith(i, vm, ARIOPENUM.LUA_OPUNM.value)
bnot = lambda i, vm: unaryArith(i, vm, ARIOPENUM.LUA_OPBNOT.value)


def llen(i, vm):
    """
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, _ = i.getAbc()
    a += 1
    b += 1
    vm.ls.Len(b)
    vm.ls.Replace(a)


def concat(i, vm):
    """
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, c = i.getAbc()
    a += 1
    b += 1
    c += 1
    n = c - b + 1
    vm.ls.CheckStack(n)
    for i in range(b, c + 1):
        vm.ls.PushValue(i)
    vm.ls.Concat(n)
    vm.ls.Replace(a)
