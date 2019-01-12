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


def move(i, vm):
    """
    R（A）：=R（B）
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, _ = i.getABC()
    a += 1
    b += 1
    vm.ls.Copy(b, a)


def jmp(i, vm):
    a, sBx = i.getAsbx()
    vm.AddPC(sBx)
    if a != 0:
        # TODO add upvalue support
        raise RuntimeError('reference to upvalue')


def loadNil(i, vm):
    """
    R(A), R(A+1), ..., R(A+B) := nil
    push nil to the top of stack
    copy (a+b) times then remove the first nil
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, _ = i.getABC()
    a += 1
    vm.ls.PushNil()
    for i in range(a, a + b + 1):
        vm.ls.Copy(-1, i)
    vm.ls.Pop(1)


def loadBool(i, vm):
    """
    R(A) := (bool)B; if (C) pc++
    :param i: Instruction
    :param vm: LuaVM
    :return:
    """
    a, b, c = i.getABC()
    a += 1
    vm.ls.PushBoolean(b != 0)
    vm.ls.Replace(a)
    if c != 0:
        vm.AddPC(1)
