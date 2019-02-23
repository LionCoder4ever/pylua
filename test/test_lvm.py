import unittest
from lvm import LuaVM
from lapi import LuaState, LUATYPE
from readChunk import Instruction, OPCODE, HandleFile
from test.testHelper import TestHelper


class TestLuaVMApi(unittest.TestCase,TestHelper):
    @classmethod
    def setUpClass(cls):
        cls.setUpFuncForVm('loop.out')

    def test_loopresult(self):
        self.assertEqual(self.getStackInfo()[0], 2550)


class TestLuaVMTableApi(unittest.TestCase,TestHelper):
    @classmethod
    def setUpClass(cls):
        cls.setUpFuncForVm('table.out')

    def test_tableresult(self):
        self.assertEqual(self.getStackInfo()[1].value, 'cBaBar3')


if __name__ == '__main__':
    unittest.main()
