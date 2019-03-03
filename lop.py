from enum import Enum

from lmath import FbToInt
from ltable import LuaTable
from lvm import LuaVM

arithoplist = [(j, i) for i, j in enumerate(['LUA_OPADD', 'LUA_OPSUB', 'LUA_OPMUL', 'LUA_OPMOD', 'LUA_OPPOW',
                                             'LUA_OPDIV', 'LUA_OPIDI', 'LUA_OPBAN', 'LUA_OPBOR', 'LUA_OPBXO',
                                             'LUA_OPSHL', 'LUA_OPSHR', 'LUA_OPUNM', 'LUA_OPBNOT'])]
ARIOPENUM = Enum('ARIOP', arithoplist)

compareoplist = [(j, i) for i, j in enumerate(['LUA_OPEQ', 'LUA_OPLT', 'LUA_OPLE'])]
COMOPENUM = Enum('COMOP', compareoplist)

MAXARG_BX = (1 << 18) - 1
MAXARG_SBX = MAXARG_BX >> 1

opcodelist = [(j, i) for i, j in enumerate(['OP_MOVE', 'OP_LOADK', 'OP_LOADKX', 'OP_LOADBOOL',
                                            'OP_LOADNIL', 'OP_GETUPVAL', 'OP_GETTABUP', 'OP_GETTABLE',
                                            'OP_SETTABUP', 'OP_SETUPVAL', 'OP_SETTABLE', 'OP_NEWTABLE',
                                            'OP_SELF', 'OP_ADD', 'OP_SUB', 'OP_MUL',
                                            'OP_MOD', 'OP_POW', 'OP_DIV', 'OP_IDIV',
                                            'OP_BAND', 'OP_BOR', 'OP_BXOR', 'OP_SHL',
                                            'OP_SHR', 'OP_UNM', 'OP_BNOT', 'OP_NOT',
                                            'OP_LEN', 'OP_CONCAT', 'OP_JMP', 'OP_EQ',
                                            'OP_LT', 'OP_LE', 'OP_TEST', 'OP_TESTSET',
                                            'OP_CALL', 'OP_TAILCALL', 'OP_RETURN', 'OP_FORLOOP',
                                            'OP_FORPREP', 'OP_TFORCALL', 'OP_TFORLOOP', 'OP_SETLIST',
                                            'OP_CLOSURE', 'OP_VARARG', 'OP_EXTRAARG'])]
OPCODE = Enum('OPCODE', opcodelist)

# OpArgN argument is not used
# OpArgU argument is used
# OpArgR argument is a register or a jump offset
# OpArgK argument is a constant or register/constant
OPARGMODE = Enum('OPARGMODE', [('OpArgN', 0), ('OpArgU', 1), ('OpArgR', 2), ('OpArgK', 3)])

OPMODE = Enum('OPMODE', [('IABC', 0), ('IABx', 1), ('IAsBx', 2), ('IAx', 3)])


# testFlag byte   operator is a test (next instruction must be a jump)
# setAFlag byte   instruction set register A
# argBMode byte   B arg mode
# argCMode byte   C arg mode
# opMode   byte   op mode
# name     string
class Opcode:
    def __init__(self, *arg):
        self.testFlag, self.setAFlag, self.argBMode, self.argCMode, self.opMode, self.name = arg


opcodes = [Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "MOVE"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "LOADK"),
           Opcode(0, 1, OPARGMODE.OpArgN.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "LOADKX"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "LOADBOOL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "LOADNIL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "GETUPVAL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "GETTABUP"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "GETTABLE"),
           Opcode(0, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SETTABUP"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "SETUPVAL"),
           Opcode(0, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SETTABLE"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "NEWTABLE"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SELF    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "ADD"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SUB"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "MUL"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "MOD"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "POW"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "DIV"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "IDIV"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BAND"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BOR"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BXOR"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SHL"),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SHR"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "UNM"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "BNOT"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "NOT"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "LEN"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgR.value, OPMODE.IABC.value, "CONCAT"),
           Opcode(0, 0, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "JMP"),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "EQ"),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "LT"),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "LE"),
           Opcode(1, 0, OPARGMODE.OpArgN.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TEST"),
           Opcode(1, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TESTSET"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "CALL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TAILCALL"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "_RETURN"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORLOOP"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORPREP"),
           Opcode(0, 0, OPARGMODE.OpArgN.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TFORCALL"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "TFORLOOP"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "SETLIST"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "CLOSURE"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "VARARG"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IAx.value, "EXTRAARG")]


class Instruction:
    def __init__(self, data):
        self.data = data

    def getOpcode(self):
        return self.data & 0x3f

    def getOpname(self):
        return opcodes[self.getOpcode()].name

    def getOpmode(self):
        return opcodes[self.getOpcode()].opMode

    def getBmode(self):
        return opcodes[self.getOpcode()].argBMode

    def getCmode(self):
        return opcodes[self.getOpcode()].argCMode

    def getOperands(self):
        opmode = self.getOpmode()
        if opmode == OPMODE.IABC.value:
            result = []
            a, b, c = self.getAbc()
            result.append(a)
            if self.getBmode() != OPARGMODE.OpArgN.value:
                if b > 0xFF:
                    b = -1 - (b & 0xFF)
                result.append(b)
            if self.getCmode() != OPARGMODE.OpArgN.value:
                if c > 0xFF:
                    c = -1 - (b & 0xFF)
                result.append(c)
            return result
        elif opmode == OPMODE.IABx.value:
            result = []
            a, bx = self.getAbx()
            result.append(a)
            if self.getBmode() != OPARGMODE.OpArgN.value:
                if self.getBmode() == OPARGMODE.OpArgK.value:
                    bx = -1 - bx
                result.append(bx)
            return result
        elif opmode == OPMODE.IAsBx.value:
            a, sbx = self.getAsbx()
            return [a, sbx]
        elif opmode == OPMODE.IAx.value:
            return [-1 - self.getAx()]
        else:
            raise TypeError('opmode not support')

    def getAbc(self):
        a = (self.data >> 6) & 0xFF
        c = (self.data >> 14) & 0x1FF
        b = (self.data >> 23) & 0x1FF
        return a, b, c

    def getAbx(self):
        a = (self.data >> 6) & 0xFF
        bx = self.data >> 14
        return a, bx

    def getAsbx(self):
        a, bx = self.getAbx()
        return a, bx - MAXARG_SBX

    def getAx(self):
        return self.data >> 6

    def getInsInfo(self):
        return '{} {}'.format(self.getOpname(), ' '.join([str(i) for i in self.getOperands()]))

    def move(self, vm):
        """
        R（A）：=R（B）
        :param vm: LuaVM
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.Copy(b, a)

    def jmp(self, vm):
        a, sBx = self.getAsbx()
        vm.AddPC(sBx)
        if a != 0:
            vm.CloseUpValues(a)

    def loadnil(self, vm):
        """
        R(A), R(A+1), ..., R(A+B) := nil
        push nil to the top of stack
        copy (a+b) times then remove the first nil
        :param vm: LuaVM
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        vm.PushNil()
        for i in range(a, a + b + 1):
            vm.Copy(-1, i)
        vm.Pop(1)

    def loadbool(self, vm):
        """
        R(A) := (bool)B; if (C) pc++
        :param vm: LuaVM
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        vm.PushBoolean(b != 0)
        vm.Replace(a)
        if c != 0:
            vm.AddPC(1)

    def loadk(self, vm):
        """

        :param vm: LuaVM
        :return:
        """
        a, bx = self.getAbx()
        a += 1
        vm.GetConst(bx)
        vm.Replace(a)

    def loadkx(self, vm):
        """
        add EXTRAARG op
        :param vm: LuaVM
        :return:
        """
        a, _ = self.getAbx()
        a += 1
        ax = Instruction(vm.Fetch()).getAx()
        vm.GetConst(ax)
        vm.Replace(a)

    def binaryrith(self, vm, op):
        """
        R(A) := RK(B) op RK(C)
        :param vm: LuaVM
        :param op: ArithOp
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        vm.GetRk(b)
        vm.GetRk(c)
        vm.Arith(op)
        vm.Replace(a)

    def unaryArith(self, vm, op):
        """
        R(A) := op R(B)
        :param vm: LuaVM
        :param op: ArithOp
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.PushValue(b)
        vm.Arith(op)
        vm.Replace(a)

    def compare(self, vm, op):
        """

        :param vm: LuaVM
        :param op: CompareOp
        :return:
        """
        a, b, c = self.getAbc()
        vm.GetRk(b)
        vm.GetRk(c)
        if vm.Compare(-2, -1, op) != (a != 0):
            vm.AddPC(1)
        vm.Pop(2)

    add = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPADD.value)
    sub = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPSUB.value)
    mul = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPMUL.value)
    mod = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPMOD.value)
    pow = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPPOW.value)
    div = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPDIV.value)
    idiv = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPIDIV.value)
    band = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPBAND.value)
    bor = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPBOR.value)
    bxor = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPBXOR.value)
    shl = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPSHL.value)
    shr = lambda self, vm: self.binaryrith(vm, ARIOPENUM.LUA_OPSHR.value)
    unm = lambda self, vm: self.unaryArith(vm, ARIOPENUM.LUA_OPUNM.value)
    bnot = lambda self, vm: self.unaryArith(vm, ARIOPENUM.LUA_OPBNOT.value)
    eq = lambda self, vm: self.compare(vm, COMOPENUM.LUA_OPEQ.value)
    lt = lambda self, vm: self.compare(vm, COMOPENUM.LUA_OPLT.value)
    le = lambda self, vm: self.compare(vm, COMOPENUM.LUA_OPLE.value)

    def len(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.Len(b)
        vm.Replace(a)

    def concat(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        b += 1
        c += 1
        n = c - b + 1
        vm.CheckStack(n)
        for i in range(b, c + 1):
            vm.PushValue(i)
        vm.Concat(n)
        vm.Replace(a)

    def lnot(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.PushBoolean(not vm.ToBoolean(b))
        vm.Replace(a)

    def testset(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        b += 1
        if vm.ToBoolean(b) == (c != 0):
            vm.Copy(b, a)
        else:
            vm.AddPC(1)

    def test(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, _, c = self.getAbc()
        a += 1
        if vm.ToBoolean(a) != (c != 0):
            vm.AddPC(1)

    def forprep(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, sBx = self.getAsbx()
        a += 1
        vm.PushValue(a)
        vm.PushValue(a + 2)
        vm.Arith(ARIOPENUM.LUA_OPSUB.value)
        vm.Replace(a)
        vm.AddPC(sBx)

    def forloop(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, sBx = self.getAsbx()
        a += 1
        vm.PushValue(a + 2)
        vm.PushValue(a)
        vm.Arith(ARIOPENUM.LUA_OPADD.value)
        vm.Replace(a)
        stepOrder = vm.ToNumber(a + 2) >= 0
        if (stepOrder and vm.Compare(a, a + 1, COMOPENUM.LUA_OPLE.value)) or (
                (not stepOrder) and vm.Compare(a + 1, a, COMOPENUM.LUA_OPLE.value)):
            vm.AddPC(sBx)
            vm.Copy(a, a + 3)

    def newtable(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        vm.CreateTable(FbToInt(b), FbToInt(c))
        vm.Replace(a)

    def gettable(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        b += 1
        vm.GetRk(c)
        vm.GetTable(b)
        vm.Replace(a)

    def settable(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        vm.GetRk(b)
        vm.GetRk(c)
        vm.SetTable(a)

    def setlist(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        if c > 0:
            c -= 1
        else:
            c = Instruction(vm.Fetch()).getAx()

        bisZero = b is 0
        if bisZero:
            b = (vm.ToInteger(-1)) - a - 1
            vm.Pop(1)

        vm.CheckStack(1)
        index = c * LuaTable.LFIELDS_PER_FLUSH

        for i in range(1, b + 1):
            index += 1
            vm.PushValue(a + i)
            vm.SetI(a, index)

        if bisZero:
            for i in range(vm.RegisterCount() + 1, vm.GetTop() + 1):
                index += 1
                vm.PushValue(i)
                vm.SetI(a, index)
            vm.SetTop(vm.RegisterCount())

    def closure(self, vm: LuaVM):
        a, bx = self.getAbx()
        a += 1
        vm.LoadProto(bx)
        vm.Replace(a)

    @staticmethod
    def _fixStack(a: int, vm: LuaVM):
        x = vm.ToInteger(-1)
        vm.Pop(1)
        vm.CheckStack(x - a)
        for i in range(a, x):
            vm.PushValue(i)
        vm.Rotate(vm.RegisterCount() + 1, x - a)

    def _pushFuncAndArgs(self, a: int, b: int, vm: LuaVM) -> int:
        if b >= 1:
            vm.CheckStack(b)
            for i in range(a, a + b):
                vm.PushValue(i)
            return b - 1
        else:
            self._fixStack(a, vm)
            return vm.GetTop() - vm.RegisterCount() - 1

    def _popResults(self, a: int, c: int, vm: LuaVM):
        if c is 1:
            pass
        elif c > 1:
            for i in range(a + c - 2, a - 1, -1):
                vm.Replace(i)
        else:
            vm.CheckStack(1)
            vm.PushInteger(a)

    def _return(self, vm: LuaVM):
        a, b, _ = self.getAbc()
        a += 1

        if b is 1:
            pass
        elif b > 1:
            vm.CheckStack(b - 1)
            for i in range(a, a + b - 1):
                vm.PushValue(i)
        else:
            self._fixStack(a, vm)

    def call(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        nArgs = self._pushFuncAndArgs(a, b, vm)
        vm.Call(nArgs, c - 1)
        self._popResults(a, c, vm)

    def vararg(self, vm: LuaVM):
        a, b, _ = self.getAbc()
        a += 1
        if b is not 1:
            vm.LoadVararg(b - 1)
            self._popResults(a, b, vm)

    def tailCall(self, vm: LuaVM):
        a, b, _ = self.getAbc()
        a += 1
        c = 0

        nArgs = self._pushFuncAndArgs(a, b, vm)
        vm.Call(nArgs, c - 1)
        self._popResults(a, c, vm)

    def self(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        b += 1
        vm.Copy(b, a + 1)
        vm.GetRk(c)
        vm.GetTable(b)
        vm.Replace(a)

    def gettabup(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        b += 1
        vm.GetRk(c)
        vm.GetTable(vm.LuaUpvalueIndex(b))
        vm.Replace(a)

    def settabup(self, vm: LuaVM):
        a, b, c = self.getAbc()
        a += 1
        vm.GetRk(b)
        vm.GetRk(c)
        vm.SetTable(vm.LuaUpvalueIndex(a))

    def getupval(self, vm: LuaVM):
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.Copy(vm.LuaUpvalueIndex(b), a)

    def setupval(self, vm: LuaVM):
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.Copy(a,vm.LuaUpvalueIndex(b))

    def execute(self, vm: LuaVM):
        action = getattr(self, str.lower(opcodes[self.getOpcode()].name))
        if action is not None:
            action(vm)
        else:
            raise RuntimeError('not support code')
