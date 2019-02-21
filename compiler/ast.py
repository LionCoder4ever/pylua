from typing import List


class Node:
    def __init__(self, name):
        self._name = name


class Stat(Node):
    pass


class Exp(Node):
    pass


class Block(Node):
    def __init__(self, lastLine: int, stats: List[Stat], retExps: List[Exp]):
        self.retExps = retExps
        self.stats = stats
        self.lastLine = lastLine


class NilExp(Exp):
    def __init__(self, line: int):
        super().__init__('NilExp')
        self.line = line


class TrueExp(Exp):
    def __init__(self, line: int):
        super().__init__('TrueExp')
        self.line = line


class FalseExp(Exp):
    def __init__(self, line: int):
        super().__init__('FalseExp')
        self.line = line


class VarargExp(Exp):
    def __init__(self, line: int):
        super().__init__('VarargExp')
        self.line = line


class NumberExp(Exp):
    def __init__(self, line: int, value: int or float):
        super().__init__('FloatExp')
        self.line = line
        self.value = value


class StringExp(Exp):
    def __init__(self, line: int, value: str):
        super().__init__('StringExp')
        self.line = line
        self.value = value


class NameExp(Exp):
    def __init__(self, line: int, name: str):
        super().__init__('NameExp')
        self.line = line
        self.name = name


class UnopExp(Exp):
    def __init__(self, line: int, op: int, exp: Exp):
        super().__init__('UnopExp')
        self.line = line
        self.op = op
        self.exp = exp


class BinopExp(Exp):
    def __init__(self, line: int, op: int, exp1: Exp, exp2: Exp):
        super().__init__('BinopExp')
        self.line = line
        self.op = op
        self.exp1 = exp1
        self.exp2 = exp2


class ConcatExp(Exp):
    def __init__(self, line: int, exps: List[Exp]):
        super().__init__('ConcatExp')
        self.line = line
        self.exps = exps


class TableConstructorExp(Exp):
    def __init__(self, line: int, lastLine: int, keyExps: List[Exp], valExps: List[Exp]):
        super().__init__('TableConstructorExp')
        self.line = line
        self.lastLine = lastLine
        self.keyExps = keyExps
        self.valExps = valExps


class FuncCallExp(Exp):
    def __init__(self, line: int, lastLine: int, prefixExp: Exp, nameExp: StringExp, args: List[Exp]):
        super().__init__('FuncCallExp')
        self.args = args
        self.nameExp = nameExp
        self.prefixExp = prefixExp
        self.lastLine = lastLine
        self.line = line


class TableAccessExp(Exp):
    def __init__(self, lastLine: int, prefixExp: Exp, keyExp: Exp):
        super().__init__('TableAccessExp')
        self.keyExp = keyExp
        self.prefixExp = prefixExp
        self.lastLine = lastLine


class ParensExp(Exp):
    def __init__(self, exp: Exp):
        super().__init__('ParensExp')
        self.exp = exp


class FuncDefExp(Exp):
    def __init__(self, line: int, lastLine: int, parList: List[str], isVararg: bool, block: Block):
        super().__init__('FuncDefExp')
        self.block = block
        self.isVararg = isVararg
        self.parList = parList
        self.lastLine = lastLine
        self.line = line


class EmptyStat(Stat):
    def __init__(self):
        super().__init__('EmptyStat')


class BreakStat(Stat):
    def __init__(self, line: int):
        super().__init__('BreakStat')
        self.line = line


class LabelStat(Stat):
    def __init__(self, labelName: str):
        super().__init__('LabelStat')
        self.labelName = labelName


class GotoStat(Stat):
    def __init__(self, labelName: str):
        super().__init__('GotoStat')
        self.labelName = labelName


class DoStat(Stat):
    def __init__(self, block: Block):
        super().__init__('DoStat')
        self.block = block


class FuncCallStat(Stat):
    def __init__(self):
        super().__init__('FuncCallStat')


class WhileStat(Stat):
    def __init__(self, exp: Exp, block: Block):
        super().__init__('WhileStat')
        self.exp = exp
        self.block = block


class RepeatStat(Stat):
    def __init__(self, exp: Exp, block: Block):
        super().__init__('RepeatStat')
        self.exp = exp
        self.block = block


class IfStat(Stat):
    def __init__(self, exp: List[Exp], block: List[Block]):
        super().__init__('IfStat')
        self.exp = exp
        self.block = block


class ForStat(Stat):
    def __init__(self, lineOfFor: int, lineOfDo: int, varName: str, initExp: Exp, limitExp: Exp, step: Exp,
                 block: Block):
        super().__init__('ForStat')
        self.block = block
        self.step = step
        self.limitExp = limitExp
        self.initExp = initExp
        self.varName = varName
        self.lineOfDo = lineOfDo
        self.lineOfFor = lineOfFor


class ForEachStat(Stat):
    def __init__(self, lineOfDo: int, nameList: List[str], expList: List[Exp], block: Block):
        super().__init__('ForEachStat')
        self.expList = expList
        self.nameList = nameList
        self.lineOfDo = lineOfDo
        self.block = block


class LocalStat(Stat):
    def __init__(self, lastLine: int, nameList: List[str], expList: List[Exp]):
        super().__init__('LocalStat')
        self.expList = expList
        self.nameList = nameList
        self.lastLine = lastLine


class AssignStat(Stat):
    def __init__(self, lastLine: int, varList: List[Exp], expList: List[Exp]):
        super().__init__('AssignStat')
        self.expList = expList
        self.varList = varList
        self.lastLine = lastLine


class GlobalFuncStat(Stat):
    def __init__(self, name: str, exp: FuncDefExp):
        super().__init__('GlobalFuncStat')
        self.name = name
        self.exp = exp


class LocalFuncStat(Stat):
    def __init__(self, name: str, exp: FuncDefExp):
        super().__init__('LocalFuncStat')
        self.name = name
        self.exp = exp
