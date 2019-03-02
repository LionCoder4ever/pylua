import unittest
from test.testHelper import TestHelper


# TODO fix unittest failure

class TestLuaVMApi(unittest.TestCase, TestHelper):
    @classmethod
    def setUpClass(cls):
        cls.setUpFuncForVm('loop.out')

    def test_loopresult(self):
        self.assertEqual(self.getValueInStack(-1), 2550)


class TestLuaVMTableApi(unittest.TestCase, TestHelper):
    @classmethod
    def setUpClass(cls):
        cls.setUpFuncForVm('table.out')

    def test_tableresult(self):
        self.assertEqual(self.getValueInStack(-1), 'cBaBar3')


if __name__ == '__main__':
    unittest.main()
