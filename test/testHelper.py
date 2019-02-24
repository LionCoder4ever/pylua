import os

from lapi import LUATYPE, LuaState


class TestHelper:
    @classmethod
    def setUpFuncForVm(cls,luaOutFilePath):
        current_path = os.path.abspath(__file__)
        parent_path = os.path.split(os.path.split(current_path)[0])[0]
        luacpath = os.path.join(parent_path, 'lua', luaOutFilePath)
        f = open(luacpath, 'rb')
        ls = LuaState()
        cls.lvm = ls
        ls.Load(f,luaOutFilePath,'b')
        ls.Call(0,0)
        f.close()

    def getValueInStack(self,index):
        return self.lvm.stack.slots[index].value

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
                result.append(source.ToString(i))
            else:
                result.append(source.TypeName(t))
        return result
