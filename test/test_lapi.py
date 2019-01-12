import unittest
from lapi import LuaState, LUATYPE, ARIOPENUM, COMOPENUM


class TestLuaStateStackApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ls = LuaState()

    def addBaseItems(self):
        self.ls.PushInteger(1)
        self.ls.PushString("2.0")
        self.ls.PushString("3.0")
        self.ls.PushNumber(4.0)

    def removeAllItems(self):
        top = self.ls.GetTop()
        if top == 1:
            self.ls.Remove(1)
        else:
            for i in range(1, self.ls.GetTop() + 1):
                self.ls.Remove(1)

    def getStackInfo(self):
        top = self.ls.GetTop()
        result = []
        for i in range(1, top + 1):
            t = self.ls.Type(i)
            if t is LUATYPE.LUA_TBOOLEAN.value:
                result.append(self.ls.ToBoolean(i))
            elif t is LUATYPE.LUA_TNUMBER.value:
                result.append(self.ls.ToNumber(i))
            elif t is LUATYPE.LUA_TSTRING.value:
                result.append(self.ls.ToString(i))
            else:
                result.append(self.ls.TypeName(t))
        return result

    def test_pushBoolean(self):
        self.ls.PushBoolean(True)
        self.assertTrue(self.getStackInfo()[-1])

    def test_pushInteger(self):
        self.ls.PushInteger(10)
        self.assertEqual(self.getStackInfo()[-1], 10)

    def test_pushNil(self):
        self.ls.PushNil()
        self.assertEqual(self.getStackInfo()[-1], 'nil')

    def test_pushString(self):
        self.ls.PushString('hello')
        self.assertEqual(self.getStackInfo()[-1], 'hello')

    def test_pushValue(self):
        prevalue = self.getStackInfo()[-4]
        self.ls.PushValue(-4)
        self.assertEqual(self.getStackInfo()[-1], prevalue)

    def test_remove(self):
        prevalue = self.getStackInfo()[-3]
        self.ls.Remove(-3)
        self.assertNotEqual(self.getStackInfo()[-3], prevalue)

    def test_replace(self):
        prevalue = self.getStackInfo()[2]
        self.ls.Replace(3)
        with self.assertRaises(ValueError):
            self.getStackInfo().index(prevalue)
        self.assertEqual(self.getStackInfo()[-1], True)

    def test_setTop(self):
        self.ls.SetTop(6)
        self.assertEqual(len(self.getStackInfo()), 6)
        self.assertEqual(self.getStackInfo()[-1], 'nil')
        self.ls.SetTop(-5)
        self.assertEqual(len(self.getStackInfo()), 2)
        self.assertEqual(self.getStackInfo()[-1], 10)

    def test_arith_add(self):
        self.addBaseItems()
        self.ls.Arith(ARIOPENUM.LUA_OPADD.value)
        self.assertEqual(self.getStackInfo()[-1], 7.0)
        self.removeAllItems()

    def test_arith_sub(self):
        self.addBaseItems()
        self.ls.Arith(ARIOPENUM.LUA_OPSUB.value)
        self.assertEqual(self.getStackInfo()[-1], -1.0)
        self.removeAllItems()

    def test_arith_bnot(self):
        self.addBaseItems()
        self.ls.Arith(ARIOPENUM.LUA_OPBNOT.value)
        self.assertEqual(self.getStackInfo()[-1], -5)
        self.removeAllItems()

    def test_arith_mod(self):
        self.addBaseItems()
        self.ls.Arith(ARIOPENUM.LUA_OPMOD.value)
        self.assertEqual(self.getStackInfo()[-1], 3)
        self.removeAllItems()

    def test_arith_band(self):
        self.ls.PushInteger(60)
        self.ls.PushInteger(13)
        self.ls.Arith(ARIOPENUM.LUA_OPBAN.value)
        self.assertEqual(self.getStackInfo()[-1], 12)
        self.removeAllItems()

    def test_arith_band(self):
        self.addBaseItems()
        self.assertEqual(self.ls.Compare(3, 4, COMOPENUM.LUA_OPEQ.value), False)
        self.removeAllItems()

    def test_concatNumber(self):
        self.ls.PushInteger(1)
        self.ls.PushInteger(2)
        self.ls.PushInteger(3)
        self.ls.Concat(2)
        self.assertEqual(self.getStackInfo()[-1], '23')
        self.removeAllItems()

    def test_concatString(self):
        self.ls.PushString('hello ')
        self.ls.PushString('world')
        self.ls.Concat(2)
        self.assertEqual(self.getStackInfo()[-1], 'hello world')
        self.removeAllItems()

    def test_len(self):
        self.ls.PushString('hello ')
        self.ls.PushString('world')
        self.ls.Len(2)
        self.assertEqual(self.getStackInfo()[-1], 5)
        self.removeAllItems()


if __name__ == '__main__':
    unittest.main()
