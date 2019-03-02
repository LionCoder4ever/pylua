import os

from lapi import LUATYPE, LuaState
from lvalue import LuaString


class TestHelper:
    @classmethod
    def setUpFuncForVm(cls, luaOutFilePath):
        cls.result = []

        def printLua(ls):
            top = ls.GetTop()
            for i in range(1, top + 1):
                t = ls.Type(i)
                if t is LUATYPE.LUA_TBOOLEAN.value:
                    cls.result.append(ls.ToBoolean(i))
                elif t is LUATYPE.LUA_TNUMBER.value:
                    cls.result.append(ls.ToNumber(i))
                elif t is LUATYPE.LUA_TSTRING.value:
                    cls.result.append(ls.ToPyString(i))
                else:
                    cls.result.append(ls.TypeName(t))
            return 0

        current_path = os.path.abspath(__file__)
        parent_path = os.path.split(os.path.split(current_path)[0])[0]
        luacpath = os.path.join(parent_path, 'lua', luaOutFilePath)
        f = open(luacpath, 'rb')
        ls = LuaState()
        ls.Register(LuaString('print'), printLua)
        ls.Load(f, luaOutFilePath, 'b')
        ls.Call(0, 0)
        f.close()

    def getValueInStack(self, index):
        return self.result[index]

    def getStackInfo(self):
        source = self.lvm
        top = source.GetTop()
        result = []
        for i in range(1, top + 1):
            t = source.Type(i)
            if t is LUATYPE.LUA_TBOOLEAN.value:
                result.append(source.ToBoolean(i))
            elif t is LUATYPE.LUA_TNUMBER.value:
                result.append(source.ToNumber(i))
            elif t is LUATYPE.LUA_TSTRING.value:
                result.append(source.ToPyString(i))
            else:
                result.append(source.TypeName(t))
        return result
