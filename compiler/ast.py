from typing import List


class Node:
    def __init__(self, name):
        self._name = name


class Exp(Node):
    pass


class Stat(Node):
    pass


class Block(Node):
    def __init__(self, lastLine: int, stats: List[Stat], retExps: List[Exp]):
        self.retExps = retExps
        self.stats = stats
        self.lastLine = lastLine


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
