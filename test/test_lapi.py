import unittest
from lapi import LuaState, ARIOPENUM, COMOPENUM, LuaArray
from ltable import LuaDict
from test.testHelper import TestHelper


class TestLuaStateStackApi(unittest.TestCase, TestHelper):
    @classmethod
    def setUpClass(cls):
        cls.lvm = LuaState()

    def addBaseItems(self):
        self.lvm.PushInteger(1)
        self.lvm.PushString("2.0")
        self.lvm.PushString("3.0")
        self.lvm.PushNumber(4.0)

    def removeAllItems(self):
        top = self.lvm.GetTop()
        if top == 1:
            self.lvm.Remove(1)
        else:
            for i in range(1, self.lvm.GetTop() + 1):
                self.lvm.Remove(1)

    def test_pushBoolean(self):
        self.lvm.PushBoolean(True)
        self.assertTrue(self.getStackInfo()[-1])

    def test_pushInteger(self):
        self.lvm.PushInteger(10)
        self.assertEqual(self.getStackInfo()[-1], 10)

    def test_pushNil(self):
        self.lvm.PushNil()
        self.assertEqual(self.getStackInfo()[-1], 'nil')

    def test_pushString(self):
        self.lvm.PushString('hello')
        self.assertEqual(self.getStackInfo()[-1], 'hello')

    def test_pushValue(self):
        prevalue = self.getStackInfo()[-4]
        self.lvm.PushValue(-4)
        self.assertEqual(self.getStackInfo()[-1], prevalue)

    def test_remove(self):
        prevalue = self.getStackInfo()[-3]
        self.lvm.Remove(-3)
        self.assertNotEqual(self.getStackInfo()[-3], prevalue)

    def test_replace(self):
        prevalue = self.getStackInfo()[2]
        self.lvm.Replace(3)
        with self.assertRaises(ValueError):
            self.getStackInfo().index(prevalue)
        self.assertEqual(self.getStackInfo()[-1], True)

    def test_setTop(self):
        self.lvm.SetTop(6)
        self.assertEqual(len(self.getStackInfo()), 6)
        self.assertEqual(self.getStackInfo()[-1], 'nil')
        self.lvm.SetTop(-5)
        self.assertEqual(len(self.getStackInfo()), 2)
        self.assertEqual(self.getStackInfo()[-1], 10)

    def test_arith_add(self):
        self.addBaseItems()
        self.lvm.Arith(ARIOPENUM.LUA_OPADD.value)
        self.assertEqual(self.getStackInfo()[-1], 7.0)
        self.removeAllItems()

    def test_arith_sub(self):
        self.addBaseItems()
        self.lvm.Arith(ARIOPENUM.LUA_OPSUB.value)
        self.assertEqual(self.getStackInfo()[-1], -1.0)
        self.removeAllItems()

    def test_arith_bnot(self):
        self.addBaseItems()
        self.lvm.Arith(ARIOPENUM.LUA_OPBNOT.value)
        self.assertEqual(self.getStackInfo()[-1], -5)
        self.removeAllItems()

    def test_arith_mod(self):
        self.addBaseItems()
        self.lvm.Arith(ARIOPENUM.LUA_OPMOD.value)
        self.assertEqual(self.getStackInfo()[-1], 3)
        self.removeAllItems()

    def test_arith_band(self):
        self.lvm.PushInteger(60)
        self.lvm.PushInteger(13)
        self.lvm.Arith(ARIOPENUM.LUA_OPBAN.value)
        self.assertEqual(self.getStackInfo()[-1], 12)
        self.removeAllItems()

    def test_arith_eq(self):
        self.addBaseItems()
        self.assertEqual(self.lvm.Compare(3, 4, COMOPENUM.LUA_OPEQ.value), False)
        self.removeAllItems()

    def test_arith_lt(self):
        self.addBaseItems()
        self.assertEqual(self.lvm.Compare(3, 4, COMOPENUM.LUA_OPLT.value), True)
        self.removeAllItems()

    def test_arith_le(self):
        self.addBaseItems()
        self.assertEqual(self.lvm.Compare(3, 4, COMOPENUM.LUA_OPLE.value), True)
        self.removeAllItems()

    def test_concatNumber(self):
        self.lvm.PushInteger(1)
        self.lvm.PushInteger(2)
        self.lvm.PushInteger(3)
        self.lvm.Concat(2)
        self.assertEqual(self.getStackInfo()[-1], '23')
        self.removeAllItems()

    def test_concatString(self):
        self.lvm.PushString('hello ')
        self.lvm.PushString('world')
        self.lvm.Concat(2)
        self.assertEqual(self.getStackInfo()[-1], 'hello world')
        self.removeAllItems()

    def test_len(self):
        self.lvm.PushString('hello ')
        self.lvm.PushString('world')
        self.lvm.Len(2)
        self.assertEqual(self.getStackInfo()[-1], 5)
        self.removeAllItems()

    def test_luaArray(self):
        self.arr = LuaArray()
        with self.assertRaises(TypeError):
            self.arr.append(11)

    def test_luaDict(self):
        self.map = LuaDict()
        with self.assertRaises(TypeError):
            self.map['errorkey'] = 'errorvalue'


if __name__ == '__main__':
    unittest.main()
