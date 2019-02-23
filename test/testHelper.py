import os
from lapi import LUATYPE, LuaState
from lvm import LuaVM
from readChunk import HandleFile, Instruction, OPCODE


class TestHelper:
    @classmethod
    def setUpFuncForVm(cls,luaOutFilePath):
        cls.lvm = None
        current_path = os.path.abspath(__file__)
        parent_path = os.path.split(os.path.split(current_path)[0])[0]
        luacpath = os.path.join(parent_path, 'lua', luaOutFilePath)
        with open(luacpath, 'rb') as f:
            handleFile = HandleFile(f)
            handleFile.readHead()
            proto = handleFile.readProtos(0)
            nRegs = proto.maxStackSize
            ls = LuaState(proto)
            ls.SetTop(nRegs)
            cls.lvm = LuaVM(ls)
            pc = cls.lvm.PC()
            inst = Instruction(cls.lvm.Fetch())
            while inst.getOpcode() is not OPCODE.OP_RETURN.value:
                inst.execute(cls.lvm)
                print("[{}] {}".format(pc + 1, inst.getOpname()))
                pc = cls.lvm.PC()
                inst = Instruction(cls.lvm.Fetch())

    def getStackInfo(self,withVM=True):
        source = self.lvm.ls if withVM else self.ls
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
