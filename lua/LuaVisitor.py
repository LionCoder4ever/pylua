# Generated from Lua.g4 by ANTLR 4.7.1
from antlr4 import *
from lua.LuaParser import LuaParser


# This class defines a complete generic visitor for a parse tree produced by LuaParser.
class LocVar():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class LuaVisitor(ParseTreeVisitor):
    locVars = []  # store the locVar

    # Visit a parse tree produced by LuaParser#chunk.
    def visitChunk(self, ctx: LuaParser.ChunkContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#block.
    def visitBlock(self, ctx: LuaParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statsemicolon.
    def visitStatsemicolon(self, ctx: LuaParser.StatsemicolonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statassign.
    def visitStatassign(self, ctx: LuaParser.StatassignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statcall.
    def visitStatcall(self, ctx: LuaParser.StatcallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statlabel.
    def visitStatlabel(self, ctx: LuaParser.StatlabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statbreak.
    def visitStatbreak(self, ctx: LuaParser.StatbreakContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statgoto.
    def visitStatgoto(self, ctx: LuaParser.StatgotoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statdo.
    def visitStatdo(self, ctx: LuaParser.StatdoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statwhile.
    def visitStatwhile(self, ctx: LuaParser.StatwhileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statrepeat.
    def visitStatrepeat(self, ctx: LuaParser.StatrepeatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statif.
    def visitStatif(self, ctx: LuaParser.StatifContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statfor.
    def visitStatfor(self, ctx: LuaParser.StatforContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statforeach.
    def visitStatforeach(self, ctx: LuaParser.StatforeachContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statglobalfunc.
    def visitStatglobalfunc(self, ctx: LuaParser.StatglobalfuncContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statlocalfunc.
    def visitStatlocalfunc(self, ctx: LuaParser.StatlocalfuncContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#statlocal.
    def visitStatlocal(self, ctx: LuaParser.StatlocalContext):
        self.visit(ctx.namelist())
        # for i in range(0,self.visit(ctx.explist())):
        #     self.visit(ctx.explist().exp())
        self.visit(ctx.explist())
        return 0
        # return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#retstat.
    def visitRetstat(self, ctx: LuaParser.RetstatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#label.
    def visitLabel(self, ctx: LuaParser.LabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#funcname.
    def visitFuncname(self, ctx: LuaParser.FuncnameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#varlist.
    def visitVarlist(self, ctx: LuaParser.VarlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#namelist.
    def visitNamelist(self, ctx: LuaParser.NamelistContext):
        nameList = [i.getText() for i in ctx.NAME()]
        for i in range(0, len(nameList)):
            localVar = LocVar(nameList[i])
            self.locVars.append(localVar)
        return nameList

    # Visit a parse tree produced by LuaParser#explist.
    def visitExplist(self, ctx: LuaParser.ExplistContext):
        expList = ctx.exp()
        for i in range(0, len(expList)):
            self.visit(ctx.exp()[i])
        return expList

    # Visit a parse tree produced by LuaParser#exp.
    def visitExp(self, ctx: LuaParser.ExpContext):
        expCount = ctx.getChildCount()
        if expCount == 1:
            rule = ctx.getChild(0).getRuleIndex()
            if rule == ctx.parser.RULE_number:
                self.visit(ctx.number())
            elif rule == ctx.parser.RULE_string:
                self.visit(ctx.string())

        elif expCount == 2:
            pass
        elif expCount == 3:
            # print(ctx.getChild(1).getText() == '+')
            pass
        else:
            raise TypeError('illegal exp')

        return

    # Visit a parse tree produced by LuaParser#prefixexp.
    def visitPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#functioncall.
    def visitFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#varOrExp.
    def visitVarOrExp(self, ctx: LuaParser.VarOrExpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#var.
    def visitVar(self, ctx: LuaParser.VarContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#varSuffix.
    def visitVarSuffix(self, ctx: LuaParser.VarSuffixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#nameAndArgs.
    def visitNameAndArgs(self, ctx: LuaParser.NameAndArgsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#args.
    def visitArgs(self, ctx: LuaParser.ArgsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#functiondef.
    def visitFunctiondef(self, ctx: LuaParser.FunctiondefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#funcbody.
    def visitFuncbody(self, ctx: LuaParser.FuncbodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#parlist.
    def visitParlist(self, ctx: LuaParser.ParlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#tableconstructor.
    def visitTableconstructor(self, ctx: LuaParser.TableconstructorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#fieldlist.
    def visitFieldlist(self, ctx: LuaParser.FieldlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#field.
    def visitField(self, ctx: LuaParser.FieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#fieldsep.
    def visitFieldsep(self, ctx: LuaParser.FieldsepContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorOr.
    def visitOperatorOr(self, ctx: LuaParser.OperatorOrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorAnd.
    def visitOperatorAnd(self, ctx: LuaParser.OperatorAndContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorComparison.
    def visitOperatorComparison(self, ctx: LuaParser.OperatorComparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorStrcat.
    def visitOperatorStrcat(self, ctx: LuaParser.OperatorStrcatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorAddSub.
    def visitOperatorAddSub(self, ctx: LuaParser.OperatorAddSubContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorMulDivMod.
    def visitOperatorMulDivMod(self, ctx: LuaParser.OperatorMulDivModContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorBitwise.
    def visitOperatorBitwise(self, ctx: LuaParser.OperatorBitwiseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorUnary.
    def visitOperatorUnary(self, ctx: LuaParser.OperatorUnaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#operatorPower.
    def visitOperatorPower(self, ctx: LuaParser.OperatorPowerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LuaParser#number.
    def visitNumber(self, ctx: LuaParser.NumberContext):
        return ctx.INT()

    # Visit a parse tree produced by LuaParser#string.
    def visitString(self, ctx: LuaParser.StringContext):
        return ctx.CHARSTRING()


del LuaParser
