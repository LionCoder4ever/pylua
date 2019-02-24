from struct import unpack
from sys import argv

from lapi import LuaState
from lvalue import LuaBoolean, LuaNil, LuaNumber, LuaString, Proto

LUA_LONG_STR_LENGTH = 254
LUA_NIL = 0
LUA_BOOLEAN = 1
LUA_NUMBER = 3
LUA_INTEGER = 19
LUA_SHORT_STR = 4
LUA_LONG_STR = 20


class HandleFile:
    def __init__(self, f):
        self.f = f
        self.sourcename = ''

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
        # proto first byte
        self.readByte()
        source = self.sourcename = self.readString() if prototype is 0 else self.sourcename

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
                constants.append(LuaNil())
            elif type == LUA_BOOLEAN:
                constants.append(LuaBoolean(self.readBoolean()))
            elif type == LUA_NUMBER:
                constants.append(LuaNumber(self.readNumber()))
            elif type == LUA_INTEGER:
                constants.append(LuaNumber(self.readInt()))
            elif type == LUA_SHORT_STR or type == LUA_LONG_STR:
                constants.append(LuaString(self.readString()))
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
        f = open(argv[1], 'rb')
        ls = LuaState()
        ls.Load(f, argv[1], 'b')
        ls.Call(0, 0)
        f.close()
