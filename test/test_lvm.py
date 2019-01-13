import unittest
import os
from lvm import LuaVM
from lapi import LuaState, LUATYPE
from readChunk import Instruction, OPCODE, HandleFile


class TestLuaVMApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lvm = None
        current_path = os.path.abspath(__file__)
        father_path = os.path.split(os.path.split(current_path)[0])[0]
        luacpath = os.path.join(father_path,'lua','luac.out')
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
                print("[{}] {}".format(pc+1,inst.getOpname()))
                pc = cls.lvm.PC()
                inst = Instruction(cls.lvm.Fetch())

    def getStackInfo(self):
        top = self.lvm.ls.GetTop()
        result = []
        for i in range(1, top + 1):
            t = self.lvm.ls.Type(i)
            if t is LUATYPE.LUA_TBOOLEAN.value:
                result.append(self.lvm.ls.ToBoolean(i))
            elif t is LUATYPE.LUA_TNUMBER.value:
                result.append(self.lvm.ls.ToNumber(i))
            elif t is LUATYPE.LUA_TSTRING.value:
                result.append(self.lvm.ls.ToString(i))
            else:
                result.append(self.ls.TypeName(t))
        return result

    def test_loopresult(self):
        self.assertEqual(self.getStackInfo()[0], 2550)


if __name__ == '__main__':
    unittest.main()
