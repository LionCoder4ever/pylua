class LuaVM:
    def __init__(self, l):
        self.ls = l

    def PC(self) -> int:
        return self.ls.pc

    def AddPC(self, n):
        self.ls.pc += n

    def Fetch(self) -> int:
        op = self.ls.proto.code[self.ls.pc]
        self.ls.pc += 1
        return op

    def GetConst(self, index):
        cons = self.ls.proto.constants[index]
        self.ls.stack.push(cons)

    # put const value or stack value
    def GetRk(self, rk):
        if rk > 0xFF:
            self.GetConst(rk & 0xFF)
        else:
            self.ls.PushValue(rk + 1)

