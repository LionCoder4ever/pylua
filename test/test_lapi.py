import unittest
from lapi import LuaState, LUATYPE


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ls = LuaState()

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
        self.assertTrue(self.getStackInfo()[len(self.getStackInfo()) - 1])

    def test_pushInteger(self):
        self.ls.PushInteger(10)
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], 10)

    def test_pushNil(self):
        self.ls.PushNil()
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], 'nil')

    def test_pushString(self):
        self.ls.PushString('hello')
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], 'hello')

    def test_pushValue(self):
        prevalue = self.getStackInfo()[-4]
        self.ls.PushValue(-4)
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], prevalue)

    def test_remove(self):
        prevalue = self.getStackInfo()[-3]
        self.ls.Remove(-3)
        self.assertNotEqual(self.getStackInfo()[-3], prevalue)

    def test_replace(self):
        prevalue = self.getStackInfo()[2]
        self.ls.Replace(3)
        with self.assertRaises(ValueError):
            self.getStackInfo().index(prevalue)
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], True)

    def test_setTop(self):
        self.ls.SetTop(6)
        self.assertEqual(len(self.getStackInfo()), 6)
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], 'nil')
        self.ls.SetTop(-5)
        self.assertEqual(len(self.getStackInfo()), 2)
        self.assertEqual(self.getStackInfo()[len(self.getStackInfo()) - 1], 10)


if __name__ == '__main__':
    unittest.main()
