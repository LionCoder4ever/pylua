from sys import argv
from struct import unpack
from enum import Enum
from lapi import LuaValue

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


opcodes = [Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "MOVE    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "LOADK   "),
           Opcode(0, 1, OPARGMODE.OpArgN.value, OPARGMODE.OpArgN.value, OPMODE.IABx.value, "LOADKX  "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "LOADBOOL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "LOADNIL "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "GETUPVAL"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "GETTABUP"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "GETTABLE"),
           Opcode(0, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SETTABUP"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "SETUPVAL"),
           Opcode(0, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SETTABLE"),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "NEWTABLE"),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SELF    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "ADD     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SUB     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "MUL     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "MOD     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "POW     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "DIV     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "IDIV    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BAND    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BOR     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "BXOR    "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SHL     "),
           Opcode(0, 1, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "SHR     "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "UNM     "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "BNOT    "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "NOT     "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "LEN     "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgR.value, OPMODE.IABC.value, "CONCAT  "),
           Opcode(0, 0, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "JMP     "),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "EQ      "),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "LT      "),
           Opcode(1, 0, OPARGMODE.OpArgK.value, OPARGMODE.OpArgK.value, OPMODE.IABC.value, "LE      "),
           Opcode(1, 0, OPARGMODE.OpArgN.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TEST    "),
           Opcode(1, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TESTSET "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "CALL    "),
           Opcode(0, 1, OPARGMODE.OpArgU.value, OPARGMODE.OpArgU.value, OPMODE.IABC.value, "TAILCALL"),
           Opcode(0, 0, OPARGMODE.OpArgU.value, OPARGMODE.OpArgN.value, OPMODE.IABC.value, "RETURN  "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORLOOP "),
           Opcode(0, 1, OPARGMODE.OpArgR.value, OPARGMODE.OpArgN.value, OPMODE.IAsBx.value, "FORPREP "),
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


LUA_LONG_STR_LENGTH = 254
LUA_NIL = 0
LUA_BOOLEAN = 1
LUA_NUMBER = 3
LUA_INTEGER = 19
LUA_SHORT_STR = 4
LUA_LONG_STR = 20


def readByte():
    return unpack('=B', f.read(1))[0]


def readString():
    length = readByte()
    if length == LUA_NIL:
        return ''
    elif length == LUA_LONG_STR_LENGTH:
        length = unpack('=d', f.read(8))
    return "".join(bytes.decode(i) for i in unpack('=%dc' % (length - 1), f.read((length - 1))))


def readCint():
    return unpack('=I', f.read(4))[0]


def readInt():
    return unpack('=Q', f.read(8))


def readBoolean():
    return unpack('=?', f.read(1))


def readNumber():
    return unpack('=d', f.read(8))


def readUpvalues():
    upvalues = []
    size = readCint()
    for i in range(size):
        upvalues.append(unpack('=2B', f.read(2)))
    return upvalues


def readLineInfo():
    lineInfo = []
    size = readCint()
    for i in range(size):
        lineInfo.append(readCint())
    return lineInfo


def readlocVars():
    locaVars = []
    size = readCint()
    for i in range(size):
        locaVar = {}
        locaVar['varName'] = readString()
        locaVar['startPc'] = readCint()
        locaVar['endPc'] = readCint()
        locaVars.append(locaVar)
    return locaVars


def readUpValueNames():
    upValueNames = []
    size = readCint()
    for i in range(size):
        upValueNames.append(readString())
    return upValueNames


class Proto:
    def __init__(self, *args):
        self.args = args
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


def readProtos(prototype):
    print('proto first byte', readByte())
    source = ''
    if prototype == 0:
        source = readString()

    line_def, last_line_def = unpack('=2I', f.read(8))

    numParms = readByte()

    isVararg = readBoolean()

    maxStackSize = readByte()

    codenum = readCint()
    code = unpack('=%dI' % codenum, f.read(codenum * 4))

    constantsnum = readCint()

    constants = []
    for i in range(constantsnum):
        type = readByte()
        if type == LUA_NIL:
            constants.append(LuaValue(LUA_NIL, None))
        elif type == LUA_BOOLEAN:
            constants.append(LuaValue(LUA_BOOLEAN, readBoolean()))
        elif type == LUA_NUMBER:
            constants.append(LuaValue(LUA_NUMBER, readNumber()))
        elif type == LUA_INTEGER:
            constants.append(LuaValue(LUA_INTEGER, readInt()))
        elif type == LUA_SHORT_STR or type == LUA_LONG_STR:
            constants.append(LuaValue(type, readString()))
        else:
            raise TypeError('type not support')

    upValues = readUpvalues()

    protosize = readCint()

    nestproto = None
    protos = []
    if protosize > 0:
        for i in range(protosize):
            nestproto = readProtos(1)
            protos.append(nestproto)
    lineinfo = readLineInfo()
    locVars = readlocVars()

    upvalueNames = readUpValueNames()
    proto = Proto(source, line_def, last_line_def, numParms, isVararg, maxStackSize, code, constants, upValues, protos,
                  lineinfo, locVars, upvalueNames)
    print(proto)


def readHead():
    sig, version, form, luac_Data, cintSize, sizetSize, instructSize, luaIntSize, luaNumSize, luac_Int, luac_Float = unpack(
        '=4scc6scccccqd', f.read(33))
    print(sig)
    print(version)
    print(form)
    print(luac_Data)
    print(cintSize)
    print(sizetSize)
    print(instructSize)
    print(luaIntSize)
    print(luaNumSize)
    print(hex(luac_Int))
    print(luac_Float)


if __name__ == '__main__':
    if len(argv) < 2:
        raise AssertionError('not enough parameter')
    elif len(argv) == 2:
        with open(argv[1], 'rb') as f:
            readHead()
            readProtos(0)
