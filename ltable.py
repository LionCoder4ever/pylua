import collections

from lmath import FloatToInteger
from lvalue import LuaValue, LUATYPE


class LuaDict(collections.Mapping):
    def __init__(self):
        self.map = {}

    def __setitem__(self, key, value):
        if not isinstance(key, LuaValue):
            raise TypeError('key must be instance of LuaValue')
        if not isinstance(value, LuaValue):
            raise TypeError('value must be instance of  LuaValue')
        self.map[key] = value

    def __getitem__(self, item):
        return self.map.get(item)

    def __iter__(self):
        return iter(self.map)

    def __len__(self):
        return len(self.map)


class LuaArray(collections.MutableSequence):
    def __init__(self):
        self.arr = []

    def __delitem__(self, key):
        del self.arr[key]

    def __getitem__(self, item):
        return self.arr[item]

    def __len__(self):
        return len(self.arr)

    def __setitem__(self, key, value):
        LuaArray.assertValue(value)
        self.arr[key] = value

    def insert(self, index, value):
        LuaArray.assertValue(value)
        self.arr.insert(index, value)

    @staticmethod
    def assertValue(value):
        if not isinstance(value, LuaValue):
            raise TypeError('value must be instance of  LuaValue')


class LuaTable(LuaValue):
    LFIELDS_PER_FLUSH = 50

    def __init__(self, narr: int, nrec: int):
        super().__init__(LUATYPE.LUA_TTABLE.value, self)
        if narr > 0:
            self.arr = LuaArray()
        if nrec > 0:
            self.map = LuaDict()

    def get(self, key: LuaValue) -> LuaValue:
        """
        if key is int or can be convert to int,get value from array
        :param key:
        :return:
        """
        key = self.floatToInteger(key)
        if type(key.value) is int and (1 <= key.value <= len(self.arr)):
            return self.arr[key.value - 1]
        return self.map.get(key)

    def put(self, key, value):
        key = self.floatToInteger(key)
        if type(key.value) is int and key.value >= 1:
            if not hasattr(self,'arr'):
                self.arr = LuaArray()
            if key.value <= len(self.arr):
                self.arr[key.value - 1] = value
                if key.value == len(self.arr) and value.value is None:
                    self.shrinkArray()
                return
            if key.value == len(self.arr) + 1:
                if hasattr(self, 'map'):
                    del self.map[key]
                if value.value is not None:
                    self.arr.append(value)
                    self.expandArray()
                return
        if value.value is not None:
            if not hasattr(self, 'map'):
                self.map = LuaDict()
            self.map[key] = value
        else:
            del self.map[key]

    def floatToInteger(self, key):
        """
        if key is float,try convert to int
        :param key:
        :return:
        """
        if key.typeOf() is LUATYPE.LUA_TNUMBER.value:
            if type(key.value) is float:
                keytoint, convert = FloatToInteger(key.value)
                if convert:
                    key.value = keytoint
                    return key
        return key

    def shrinkArray(self):
        for i in range(len(self.arr) - 1, -1, -1):
            if self.arr[i].value is None:
                self.arr.pop()

    def expandArray(self):
        """
        move item in map to arr
        :return:
        """
        idx = len(self.arr) + 1
        if hasattr(self, 'map'):
            for i in self.map.keys():
                if int(i.value) is idx:
                    self.arr.append(self.map[i])
                    del self.map[i]
                    idx += 1
                else:
                    break

    def len(self) -> int:
        return len(self.arr)
