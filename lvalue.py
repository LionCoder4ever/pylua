from enum import Enum

from lmath import FloatToInteger

luatypelist = [(j, i) for i, j in enumerate(['LUA_TNONE', 'LUA_TNIL', 'LUA_TBOOLEAN', 'LUA_TLIGHTUSERDATA',
                                             'LUA_TNUMBER', 'LUA_TSTRING', 'LUA_TTABLE', 'LUA_TFUNCTION',
                                             'LUA_TUSERDATA', 'LUA_TTHREAD'])]

LUATYPE = Enum('LUATYPE', luatypelist)


class Proto:
    def __init__(self, *args):
        self.source, self.lineDef, self.lastLineDef, self.numParms, self.isVararg \
            , self.maxStackSize, self.code, self.constants, self.upvalues, self.protos, self.lineinfo \
            , self.locVars, self.upValueNames = args

    def getCodeList(self):
        # 0x{:08x}
        from lop import Instruction
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
           self.lineDef,
           self.lastLineDef,
           len(self.code),
           self.numParms,
           '+' if self.isVararg else '',
           self.maxStackSize,
           len(self.upvalues),
           len(self.locVars),
           len(self.constants),
           len(self.protos)
           ) + self.getCodeList() + self.getConstants() + self.getLocals() + self.getUpvalues()


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
        return LuaNil()

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


class LuaNil(LuaValue):
    def __init__(self):
        super().__init__(LUATYPE.LUA_TNIL.value, None)


class LuaBoolean(LuaValue):
    def __init__(self, value: bool):
        super().__init__(LUATYPE.LUA_TBOOLEAN.value, value)


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


class LuaClosure(LuaValue):
    def __init__(self, proto: Proto, pyFunc=None):
        super().__init__(LUATYPE.LUA_TFUNCTION.value, proto if proto is not None else pyFunc)
        self.pyFunc = pyFunc
        self.upvalues = proto.upvalues if proto is not None else []
