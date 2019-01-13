from sys import argv
from struct import unpack
from enum import Enum
from lapi import LuaValue, ARIOPENUM, COMOPENUM, LuaState, LUATYPE
from lvm import LuaVM

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
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "CALL    "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TAILCALL"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "RETURN  "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORLOOP"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORPREP"),
           Opcode(0, 0, OPARGMODE.OpArgN.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TFORCALL"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "TFORLOOP"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "SETLIST "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "CLOSURE "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "VARARG  "),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IAx.value, "EXTRAARG")]

MAXARG_BX = (1 << 18) - 1
MAXARG_SBX = MAXARG_BX >> 1


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
                print('bx:::::', bx)
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
        vm.ls.Copy(b, a)

    def jmp(self, vm):
        a, sBx = self.getAsbx()
        vm.AddPC(sBx)
        if a != 0:
            # TODO add upvalue support
            raise RuntimeError('reference to upvalue')

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
        vm.ls.PushNil()
        for i in range(a, a + b + 1):
            vm.ls.Copy(-1, i)
        vm.ls.Pop(1)

    def loadbool(self, vm):
        """
        R(A) := (bool)B; if (C) pc++
        :param vm: LuaVM
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        vm.ls.PushBoolean(b != 0)
        vm.ls.Replace(a)
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
        vm.ls.Replace(a)

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
        vm.ls.Replace(a)

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
        vm.ls.Arith(op)
        vm.ls.Replace(a)

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
        vm.ls.PushValue(b)
        vm.ls.Arith(op)
        vm.ls.Replace(a)

    def compare(self, vm, op):
        """

        :param vm: LuaVM
        :param op: CompareOp
        :return:
        """
        a, b, c = self.getAbc()
        vm.GetRk(b)
        vm.GetRk(c)
        if vm.ls.Compare(-2, -1, op) != (a != 0):
            vm.AddPC(1)
        vm.ls.Pop(2)

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
        vm.ls.Len(b)
        vm.ls.Replace(a)

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
        vm.ls.CheckStack(n)
        for i in range(b, c + 1):
            vm.ls.PushValue(i)
        vm.ls.Concat(n)
        vm.ls.Replace(a)

    def lnot(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, _ = self.getAbc()
        a += 1
        b += 1
        vm.ls.PushBoolean(not vm.ls.ToBoolean(b))
        vm.ls.Replace(a)

    def testset(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, b, c = self.getAbc()
        a += 1
        b += 1
        if vm.ls.ToBoolean(b) == (c != 0):
            vm.ls.Copy(b, a)
        else:
            vm.AddPC(1)

    def test(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, _, c = self.getAbc()
        a += 1
        if vm.ls.ToBoolean(a) != (c != 0):
            vm.AddPC(1)

    def forprep(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, sBx = self.getAsbx()
        a += 1
        vm.ls.PushValue(a)
        vm.ls.PushValue(a + 2)
        vm.ls.Arith(ARIOPENUM.LUA_OPSUB.value)
        vm.ls.Replace(a)
        vm.AddPC(sBx)

    def forloop(self, vm):
        """
        :param vm: LuaVM
        :return:
        """
        a, sBx = self.getAsbx()
        a += 1
        vm.ls.PushValue(a + 2)
        vm.ls.PushValue(a)
        vm.ls.Arith(ARIOPENUM.LUA_OPADD.value)
        vm.ls.Replace(a)
        stepOrder = vm.ls.ToNumber(a + 2) >= 0
        if (stepOrder and vm.ls.Compare(a, a + 1, COMOPENUM.LUA_OPLE.value)) or (
                (not stepOrder) and vm.ls.Compare(a + 1, a, COMOPENUM.LUA_OPLE.value)):
            vm.AddPC(sBx)
            vm.ls.Copy(a, a + 3)

    def execute(self, vm):
        action = getattr(self, str.lower(opcodes[self.getOpcode()].name))
        if action is not None:
            action(vm)
        else:
            raise RuntimeError('not support code')


LUA_LONG_STR_LENGTH = 254
LUA_NIL = 0
LUA_BOOLEAN = 1
LUA_NUMBER = 3
LUA_INTEGER = 19
LUA_SHORT_STR = 4
LUA_LONG_STR = 20


class Proto:
    def __init__(self, *args):
        self.source, self.line_def, self.last_line_def, self.numParms, self.isVararg \
            , self.maxStackSize, self.code, self.constants, self.upvalues, self.protos, self.lineinfo \
            , self.locVars, self.upValueNames = args

    def getCodeList(self):
        # 0x{:08x}
        return '\n'.join(['\t{}   [{}]   {}'.format(i + 1, self.lineinfo[i], Instruction(j).getInsInfo()) for i, j in
                          enumerate(self.code)])
        # ins = Instruction(self.code)
        # op = ins.getOpcode()
        # # if op ===

    def getConstants(self):
        return '\nconstants ({}):\n'.format(len(self.constants)) + ''.join(
            ['\t{} {}\n'.format(i + 1, j) for i, j in enumerate(self.constants)])

    def getLocals(self):
        return '\nlocals ({}):\n'.format(len(self.locVars)) + ''.join(
            ['\t{} {} {} {}\n'.format(i + 1, j['varName'], j['startPc'] + 1, j['endPc'] + 1) for i, j in
             enumerate(self.locVars)])

    def getUpvalues(self):
        return '\nupvalues ({}):\n'.format(len(self.upvalues)) + ''.join(
            ['\t{} {} {} {}\n'.format(i + 1, self.upValueNames[i], j[0], j[1]) for i, j in enumerate(self.upvalues)])

    def __str__(self):
        return """{0} <{1} {2},{3}> ({4} instructions) \n\
{5}{6}params, {7} slots, {8} upvalues, {9} locals, {10} constants, {11} functions\n\
""".format('main' if self.source else '',
           self.source,
           self.line_def,
           self.last_line_def,
           len(self.code),
           self.numParms,
           '+' if self.isVararg else '',
           self.maxStackSize,
           len(self.upvalues),
           len(self.locVars),
           len(self.constants),
           len(self.protos)
           ) + self.getCodeList() + self.getConstants() + self.getLocals() + self.getUpvalues()


class HandleFile:
    def __init__(self, f):
        self.f = f

    def readByte(self):
        return unpack('=B', self.f.read(1))[0]

    def readString(self):
        length = self.readByte()
        if length == LUA_NIL:
            return ''
        elif length == LUA_LONG_STR_LENGTH:
            length = unpack('=d', self.f.read(8))
        return "".join(bytes.decode(i) for i in unpack('=%dc' % (length - 1), self.f.read((length - 1))))

    def readCint(self):
        return unpack('=I', self.f.read(4))[0]

    def readInt(self):
        return unpack('=Q', self.f.read(8))[0]

    def readBoolean(self):
        return unpack('=?', self.f.read(1))[0]

    def readNumber(self):
        return unpack('=d', self.f.read(8))[0]

    def readUpvalues(self):
        upvalues = []
        size = self.readCint()
        for i in range(size):
            upvalues.append(unpack('=2B', self.f.read(2)))
        return upvalues

    def readLineInfo(self):
        lineInfo = []
        size = self.readCint()
        for i in range(size):
            lineInfo.append(self.readCint())
        return lineInfo

    def readlocVars(self):
        locaVars = []
        size = self.readCint()
        for i in range(size):
            locaVar = {}
            locaVar['varName'] = self.readString()
            locaVar['startPc'] = self.readCint()
            locaVar['endPc'] = self.readCint()
            locaVars.append(locaVar)
        return locaVars

    def readUpValueNames(self):
        upValueNames = []
        size = self.readCint()
        for i in range(size):
            upValueNames.append(self.readString())
        return upValueNames

    def readProtos(self, prototype):
        print('proto first byte', self.readByte())
        source = ''
        if prototype == 0:
            source = self.readString()

        line_def, last_line_def = unpack('=2I', self.f.read(8))

        numParms = self.readByte()

        isVararg = self.readBoolean()

        maxStackSize = self.readByte()

        codenum = self.readCint()
        code = unpack('=%dI' % codenum, self.f.read(codenum * 4))

        constantsnum = self.readCint()

        constants = []
        for i in range(constantsnum):
            type = self.readByte()
            if type == LUA_NIL:
                constants.append(LuaValue(LUATYPE.LUA_TNIL.value, None))
            elif type == LUA_BOOLEAN:
                constants.append(LuaValue(LUATYPE.LUA_TBOOLEAN.value, self.readBoolean()))
            elif type == LUA_NUMBER:
                constants.append(LuaValue(LUATYPE.LUA_TNUMBER.value, self.readNumber()))
            elif type == LUA_INTEGER:
                constants.append(LuaValue(LUATYPE.LUA_TNUMBER.value, self.readInt()))
            elif type == LUA_SHORT_STR or type == LUA_LONG_STR:
                constants.append(LuaValue(LUATYPE.LUA_TSTRING.value, self.readString()))
            else:
                raise TypeError('type not support')

        upValues = self.readUpvalues()

        protosize = self.readCint()

        nestproto = None
        protos = []
        if protosize > 0:
            for i in range(protosize):
                nestproto = self.readProtos(1)
                protos.append(nestproto)
        lineinfo = self.readLineInfo()
        locVars = self.readlocVars()

        upvalueNames = self.readUpValueNames()
        proto = Proto(source, line_def, last_line_def, numParms, isVararg, maxStackSize, code, constants, upValues,
                      protos,
                      lineinfo, locVars, upvalueNames)
        return proto

    def readHead(self):
        """
        read luac out file header
        """
        sig, version, form, luac_Data, cintSize, sizetSize, instructSize, luaIntSize, luaNumSize, luac_Int, luac_Float = unpack(
            '=4scc6scccccqd', self.f.read(33))


if __name__ == '__main__':
    if len(argv) < 2:
        raise AssertionError('not enough parameter')
    elif len(argv) == 2:
        with open(argv[1], 'rb') as f:
            handleFile = HandleFile(f)
            handleFile.readHead()
            proto = handleFile.readProtos(0)
            nRegs = proto.maxStackSize
            ls = LuaState(proto)
            ls.SetTop(nRegs)
            lvm = LuaVM(ls)
            pc = lvm.PC()
            inst = Instruction(lvm.Fetch())
            while inst.getOpcode() is not OPCODE.OP_RETURN.value:
                inst.execute(lvm)
                print("[{}] {}".format(pc + 1, inst.getOpname()))
                pc = lvm.PC()
                inst = Instruction(lvm.Fetch())
