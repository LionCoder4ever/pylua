# Generated from Lua.g4 by ANTLR 4.7.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .LuaParser import LuaParser
else:
    from LuaParser import LuaParser


# This class defines a complete listener for a parse tree produced by LuaParser.
class LuaListener(ParseTreeListener):

    # Enter a parse tree produced by LuaParser#chunk.
    def enterChunk(self, ctx: LuaParser.ChunkContext):
        pass

    # Exit a parse tree produced by LuaParser#chunk.
    def exitChunk(self, ctx: LuaParser.ChunkContext):
        pass

    # Enter a parse tree produced by LuaParser#block.
    def enterBlock(self, ctx: LuaParser.BlockContext):
        pass

    # Exit a parse tree produced by LuaParser#block.
    def exitBlock(self, ctx: LuaParser.BlockContext):
        pass

    # Enter a parse tree produced by LuaParser#statsemicolon.
    def enterStatsemicolon(self, ctx: LuaParser.StatsemicolonContext):
        pass

    # Exit a parse tree produced by LuaParser#statsemicolon.
    def exitStatsemicolon(self, ctx: LuaParser.StatsemicolonContext):
        pass

    # Enter a parse tree produced by LuaParser#statassign.
    def enterStatassign(self, ctx: LuaParser.StatassignContext):
        pass

    # Exit a parse tree produced by LuaParser#statassign.
    def exitStatassign(self, ctx: LuaParser.StatassignContext):
        pass

    # Enter a parse tree produced by LuaParser#statcall.
    def enterStatcall(self, ctx: LuaParser.StatcallContext):
        pass

    # Exit a parse tree produced by LuaParser#statcall.
    def exitStatcall(self, ctx: LuaParser.StatcallContext):
        pass

    # Enter a parse tree produced by LuaParser#statlabel.
    def enterStatlabel(self, ctx: LuaParser.StatlabelContext):
        pass

    # Exit a parse tree produced by LuaParser#statlabel.
    def exitStatlabel(self, ctx: LuaParser.StatlabelContext):
        pass

    # Enter a parse tree produced by LuaParser#statbreak.
    def enterStatbreak(self, ctx: LuaParser.StatbreakContext):
        pass

    # Exit a parse tree produced by LuaParser#statbreak.
    def exitStatbreak(self, ctx: LuaParser.StatbreakContext):
        pass

    # Enter a parse tree produced by LuaParser#statgoto.
    def enterStatgoto(self, ctx: LuaParser.StatgotoContext):
        pass

    # Exit a parse tree produced by LuaParser#statgoto.
    def exitStatgoto(self, ctx: LuaParser.StatgotoContext):
        pass

    # Enter a parse tree produced by LuaParser#statdo.
    def enterStatdo(self, ctx: LuaParser.StatdoContext):
        pass

    # Exit a parse tree produced by LuaParser#statdo.
    def exitStatdo(self, ctx: LuaParser.StatdoContext):
        pass

    # Enter a parse tree produced by LuaParser#statwhile.
    def enterStatwhile(self, ctx: LuaParser.StatwhileContext):
        pass

    # Exit a parse tree produced by LuaParser#statwhile.
    def exitStatwhile(self, ctx: LuaParser.StatwhileContext):
        pass

    # Enter a parse tree produced by LuaParser#statrepeat.
    def enterStatrepeat(self, ctx: LuaParser.StatrepeatContext):
        pass

    # Exit a parse tree produced by LuaParser#statrepeat.
    def exitStatrepeat(self, ctx: LuaParser.StatrepeatContext):
        pass

    # Enter a parse tree produced by LuaParser#statif.
    def enterStatif(self, ctx: LuaParser.StatifContext):
        pass

    # Exit a parse tree produced by LuaParser#statif.
    def exitStatif(self, ctx: LuaParser.StatifContext):
        pass

    # Enter a parse tree produced by LuaParser#statfor.
    def enterStatfor(self, ctx: LuaParser.StatforContext):
        pass

    # Exit a parse tree produced by LuaParser#statfor.
    def exitStatfor(self, ctx: LuaParser.StatforContext):
        pass

    # Enter a parse tree produced by LuaParser#statforeach.
    def enterStatforeach(self, ctx: LuaParser.StatforeachContext):
        pass

    # Exit a parse tree produced by LuaParser#statforeach.
    def exitStatforeach(self, ctx: LuaParser.StatforeachContext):
        pass

    # Enter a parse tree produced by LuaParser#statglobalfunc.
    def enterStatglobalfunc(self, ctx: LuaParser.StatglobalfuncContext):
        pass

    # Exit a parse tree produced by LuaParser#statglobalfunc.
    def exitStatglobalfunc(self, ctx: LuaParser.StatglobalfuncContext):
        pass

    # Enter a parse tree produced by LuaParser#statlocalfunc.
    def enterStatlocalfunc(self, ctx: LuaParser.StatlocalfuncContext):
        pass

    # Exit a parse tree produced by LuaParser#statlocalfunc.
    def exitStatlocalfunc(self, ctx: LuaParser.StatlocalfuncContext):
        pass

    # Enter a parse tree produced by LuaParser#statlocal.
    def enterStatlocal(self, ctx: LuaParser.StatlocalContext):
        pass

    # Exit a parse tree produced by LuaParser#statlocal.
    def exitStatlocal(self, ctx: LuaParser.StatlocalContext):
        pass

    # Enter a parse tree produced by LuaParser#retstat.
    def enterRetstat(self, ctx: LuaParser.RetstatContext):
        pass

    # Exit a parse tree produced by LuaParser#retstat.
    def exitRetstat(self, ctx: LuaParser.RetstatContext):
        pass

    # Enter a parse tree produced by LuaParser#label.
    def enterLabel(self, ctx: LuaParser.LabelContext):
        pass

    # Exit a parse tree produced by LuaParser#label.
    def exitLabel(self, ctx: LuaParser.LabelContext):
        pass

    # Enter a parse tree produced by LuaParser#funcname.
    def enterFuncname(self, ctx: LuaParser.FuncnameContext):
        pass

    # Exit a parse tree produced by LuaParser#funcname.
    def exitFuncname(self, ctx: LuaParser.FuncnameContext):
        pass

    # Enter a parse tree produced by LuaParser#varlist.
    def enterVarlist(self, ctx: LuaParser.VarlistContext):
        pass

    # Exit a parse tree produced by LuaParser#varlist.
    def exitVarlist(self, ctx: LuaParser.VarlistContext):
        pass

    # Enter a parse tree produced by LuaParser#namelist.
    def enterNamelist(self, ctx: LuaParser.NamelistContext):
        pass

    # Exit a parse tree produced by LuaParser#namelist.
    def exitNamelist(self, ctx: LuaParser.NamelistContext):
        pass

    # Enter a parse tree produced by LuaParser#explist.
    def enterExplist(self, ctx: LuaParser.ExplistContext):
        pass

    # Exit a parse tree produced by LuaParser#explist.
    def exitExplist(self, ctx: LuaParser.ExplistContext):
        pass

    # Enter a parse tree produced by LuaParser#exp.
    def enterExp(self, ctx: LuaParser.ExpContext):
        pass

    # Exit a parse tree produced by LuaParser#exp.
    def exitExp(self, ctx: LuaParser.ExpContext):
        pass

    # Enter a parse tree produced by LuaParser#prefixexp.
    def enterPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        pass

    # Exit a parse tree produced by LuaParser#prefixexp.
    def exitPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        pass

    # Enter a parse tree produced by LuaParser#functioncall.
    def enterFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        pass

    # Exit a parse tree produced by LuaParser#functioncall.
    def exitFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        pass

    # Enter a parse tree produced by LuaParser#varOrExp.
    def enterVarOrExp(self, ctx: LuaParser.VarOrExpContext):
        pass

    # Exit a parse tree produced by LuaParser#varOrExp.
    def exitVarOrExp(self, ctx: LuaParser.VarOrExpContext):
        pass

    # Enter a parse tree produced by LuaParser#var.
    def enterVar(self, ctx: LuaParser.VarContext):
        pass

    # Exit a parse tree produced by LuaParser#var.
    def exitVar(self, ctx: LuaParser.VarContext):
        pass

    # Enter a parse tree produced by LuaParser#varSuffix.
    def enterVarSuffix(self, ctx: LuaParser.VarSuffixContext):
        pass

    # Exit a parse tree produced by LuaParser#varSuffix.
    def exitVarSuffix(self, ctx: LuaParser.VarSuffixContext):
        pass

    # Enter a parse tree produced by LuaParser#nameAndArgs.
    def enterNameAndArgs(self, ctx: LuaParser.NameAndArgsContext):
        pass

    # Exit a parse tree produced by LuaParser#nameAndArgs.
    def exitNameAndArgs(self, ctx: LuaParser.NameAndArgsContext):
        pass

    # Enter a parse tree produced by LuaParser#args.
    def enterArgs(self, ctx: LuaParser.ArgsContext):
        pass

    # Exit a parse tree produced by LuaParser#args.
    def exitArgs(self, ctx: LuaParser.ArgsContext):
        pass

    # Enter a parse tree produced by LuaParser#functiondef.
    def enterFunctiondef(self, ctx: LuaParser.FunctiondefContext):
        pass

    # Exit a parse tree produced by LuaParser#functiondef.
    def exitFunctiondef(self, ctx: LuaParser.FunctiondefContext):
        pass

    # Enter a parse tree produced by LuaParser#funcbody.
    def enterFuncbody(self, ctx: LuaParser.FuncbodyContext):
        pass

    # Exit a parse tree produced by LuaParser#funcbody.
    def exitFuncbody(self, ctx: LuaParser.FuncbodyContext):
        pass

    # Enter a parse tree produced by LuaParser#parlist.
    def enterParlist(self, ctx: LuaParser.ParlistContext):
        pass

    # Exit a parse tree produced by LuaParser#parlist.
    def exitParlist(self, ctx: LuaParser.ParlistContext):
        pass

    # Enter a parse tree produced by LuaParser#tableconstructor.
    def enterTableconstructor(self, ctx: LuaParser.TableconstructorContext):
        pass

    # Exit a parse tree produced by LuaParser#tableconstructor.
    def exitTableconstructor(self, ctx: LuaParser.TableconstructorContext):
        pass

    # Enter a parse tree produced by LuaParser#fieldlist.
    def enterFieldlist(self, ctx: LuaParser.FieldlistContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldlist.
    def exitFieldlist(self, ctx: LuaParser.FieldlistContext):
        pass

    # Enter a parse tree produced by LuaParser#field.
    def enterField(self, ctx: LuaParser.FieldContext):
        pass

    # Exit a parse tree produced by LuaParser#field.
    def exitField(self, ctx: LuaParser.FieldContext):
        pass

    # Enter a parse tree produced by LuaParser#fieldsep.
    def enterFieldsep(self, ctx: LuaParser.FieldsepContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldsep.
    def exitFieldsep(self, ctx: LuaParser.FieldsepContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorOr.
    def enterOperatorOr(self, ctx: LuaParser.OperatorOrContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorOr.
    def exitOperatorOr(self, ctx: LuaParser.OperatorOrContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorAnd.
    def enterOperatorAnd(self, ctx: LuaParser.OperatorAndContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAnd.
    def exitOperatorAnd(self, ctx: LuaParser.OperatorAndContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorComparison.
    def enterOperatorComparison(self, ctx: LuaParser.OperatorComparisonContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorComparison.
    def exitOperatorComparison(self, ctx: LuaParser.OperatorComparisonContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorStrcat.
    def enterOperatorStrcat(self, ctx: LuaParser.OperatorStrcatContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorStrcat.
    def exitOperatorStrcat(self, ctx: LuaParser.OperatorStrcatContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorAddSub.
    def enterOperatorAddSub(self, ctx: LuaParser.OperatorAddSubContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAddSub.
    def exitOperatorAddSub(self, ctx: LuaParser.OperatorAddSubContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorMulDivMod.
    def enterOperatorMulDivMod(self, ctx: LuaParser.OperatorMulDivModContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorMulDivMod.
    def exitOperatorMulDivMod(self, ctx: LuaParser.OperatorMulDivModContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorBitwise.
    def enterOperatorBitwise(self, ctx: LuaParser.OperatorBitwiseContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorBitwise.
    def exitOperatorBitwise(self, ctx: LuaParser.OperatorBitwiseContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorUnary.
    def enterOperatorUnary(self, ctx: LuaParser.OperatorUnaryContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorUnary.
    def exitOperatorUnary(self, ctx: LuaParser.OperatorUnaryContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorPower.
    def enterOperatorPower(self, ctx: LuaParser.OperatorPowerContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorPower.
    def exitOperatorPower(self, ctx: LuaParser.OperatorPowerContext):
        pass

    # Enter a parse tree produced by LuaParser#number.
    def enterNumber(self, ctx: LuaParser.NumberContext):
        pass

    # Exit a parse tree produced by LuaParser#number.
    def exitNumber(self, ctx: LuaParser.NumberContext):
        pass

    # Enter a parse tree produced by LuaParser#string.
    def enterString(self, ctx: LuaParser.StringContext):
        pass

    # Exit a parse tree produced by LuaParser#string.
    def exitString(self, ctx: LuaParser.StringContext):
        pass
