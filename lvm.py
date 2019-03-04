from lvalue import LuaClosure


class LuaVM:
    # def PC(self) -> int:
    #     return self.stack.pc

    def AddPC(self, n):
        self.stack.pc += n

    def Fetch(self) -> int:
        op = self.stack.closure.value.code[self.stack.pc]
        self.stack.pc += 1
        return op

    def GetConst(self, index):
        cons = self.stack.closure.value.constants[index]
        self.stack.push(cons)

    # put const value or stack value
    def GetRk(self, rk):
        if rk > 0xFF:
            self.GetConst(rk & 0xFF)
        else:
            self.PushValue(rk + 1)

    def RegisterCount(self) -> int:
        return self.stack.closure.value.maxStackSize

    def LoadVararg(self,n:int):
        if n < 0:
            n = len(self.stack.varargs)
        self.stack.check(n)
        self.stack.pushN(self.stack.varargs,n)

    def LoadProto(self,index:int):
        proto = self.stack.closure.value.protos[index]
        closure = LuaClosure(proto)
        self.stack.push(closure)
        for i in range(len(proto.upvalues)):
            upvalueItem = proto.upvalues[i]
            if upvalueItem[0] is 1:
                if self.stack.openuvs is None:
                    self.stack.openuvs = {}
                if self.stack.openuvs.get(upvalueItem[1],None) is not None:
                    closure.upvalues[i] = self.stack.openuvs.get(upvalueItem[1],None)
                else:
                    closure.upvalues[i] = self.stack.slots[upvalueItem[1]]
                    self.stack.openuvs[upvalueItem[1]] = closure.upvalues[i]
            else:
                closure.upvalues[i] = self.stack.closure.upvalues[upvalueItem[1]]
