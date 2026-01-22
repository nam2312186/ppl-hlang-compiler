"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *

class ASTGeneration:
    def visit(self, ctx):
        pass

class ASTGeneration(HLangVisitor):
    #============= PROGRAM STRUCTURE =============
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        # Grammar : program : decllist EOF ;
        const_decls=[]
        func_decls=[]
        if ctx.decllist():
            const_decls,func_decls = self.visitDecllist(ctx.decllist())

        return Program(const_decls, func_decls)
                       
    def visitDecllist(self, ctx: HLangParser.DecllistContext):
        #  decllist: decl decllist | ;
        const_decls = []
        func_decls = []

        if ctx.decl():
            decl_node = self.visit(ctx.decl())
            if isinstance(decl_node, ConstDecl):
                const_decls.append(decl_node)
            elif isinstance(decl_node, FuncDecl):
                func_decls.append(decl_node)
            if ctx.decllist():
                remaining_const,remaining_func = self.visitDecllist(ctx.decllist())
                const_decls += remaining_const
                func_decls += remaining_func
               
        return const_decls, func_decls
    
    def visitDecl(self, ctx: HLangParser.DeclContext):
        # Grammar : decl : constdecl | funcdecl ;

        if ctx.constdecl():
            return self.visitConstdecl(ctx.constdecl())
        elif ctx.funcdecl():
            return self.visitFuncdecl(ctx.funcdecl())
        return None
    
    #============= DECLARATION =============

    def visitConstdecl(self, ctx: HLangParser.ConstdeclContext):
        # constdecl: CONST ID typeanno ASSIGN expr SEMI ;
        name = ctx.ID().getText()
        value = self.visitExpr(ctx.expr())
        
        if ctx.typeanno() and ctx.typeanno().type_():
            type_annotation = self.visitTypeanno(ctx.typeanno())
            return ConstDecl(name, type_annotation, value)
        else:
            return ConstDecl(name, None,value)
    
    def visitFuncdecl(self, ctx:HLangParser.FuncdeclContext):
        # funcdecl: FUNC ID LPAREN paramlist RPAREN ARROW type body ;
        name = ctx.ID().getText()
        params = []
        if ctx.paramlist():
            params = self.visitParamlist(ctx.paramlist())
        
        return_type =self.visitType(ctx.type_())

        body = []
        if ctx.body():
            body = self.visitBody(ctx.body())

        return FuncDecl(name, params, return_type, body)
    

    # ============= PARAMETERS =============
    def visitParamlist(self,ctx : HLangParser.ParamlistContext):
        # paramlist: paramprime | ;
        if ctx.paramprime():
            return self.visitParamprime(ctx.paramprime())
        return []
    
    def visitParamprime(self, ctx : HLangParser.ParamprimeContext):
        # paramprime: param COMMA paramprime | param ;
        params = []
        if ctx.param():
            params.append(self.visitParam(ctx.param()))
        if ctx.paramprime():
            params += self.visitParamprime(ctx.paramprime())
        return params
    
    def visitParam(self, ctx:HLangParser.ParamContext):
        # param: ID COLON type ;
        name = ctx.ID().getText()
        param_type=self.visitType(ctx.type_())
        return Param(name, param_type)
    
    # ============= TYPE SYSTEM =============
    def visitType(self, ctx:HLangParser.TypeContext ):
        # type : primetype | arraytype ;
        if ctx.primetype():
            return self.visitPrimetype(ctx.primetype())
        elif ctx.arraytype():
            return self.visitArraytype(ctx.arraytype())
        
    def visitPrimetype(self, ctx:HLangParser.PrimetypeContext):
        # primetype: INT | FLOAT | BOOL | STRING | VOID ;
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        elif ctx.VOID():
            return VoidType()
        
    def visitArraytype(self, ctx: HLangParser.ArraytypeContext):
        # arraytype: LBRACK type SEMI INTLIT RBRACK ;
        element_type = self.visitType(ctx.type_())
        size = int(ctx.INTLIT().getText())
        return ArrayType(element_type, size)
    
    def visitTypeanno(self, ctx: HLangParser.TypeannoContext):
        # typeanno: COLON type | ;
        if ctx.type_():
            return self.visitType(ctx.type_())
        return None
    
    # ============= FUNCTION BODY =============

    def visitBody(self, ctx: HLangParser.BodyContext):
        # body: LBRACE stmtlist RBRACE ;
        if ctx.stmtlist():
            return self.visitStmtlist(ctx.stmtlist())
        return []
    
    def visitStmtlist(self, ctx: HLangParser.StmtlistContext):
        # stmtlist: stmt stmtlist | ;
        statements = []
        if ctx.stmt():
            stnt_node = self.visitStmt(ctx.stmt())
            if stnt_node:
                statements.append(stnt_node)
        if ctx.stmtlist():
            statements += self.visitStmtlist(ctx.stmtlist())
        return statements



    # ============ STATEMENTS =============
    def visitStmt(self,ctx: HLangParser.StmtContext):
        '''stmt: vardecl | assignstmt | ifstmt | whilestmt | forstmt 
    | breakstmt | contstmt | returnstmt | exprstmt | blockstmt ;'''
        
        if ctx.vardecl():
            return self.visitVardecl(ctx.vardecl())
        elif ctx.assignstmt():
            return self.visitAssignstmt(ctx.assignstmt())
        elif ctx.ifstmt():
            return self.visitIfstmt(ctx.ifstmt())
        elif ctx.whilestmt():
            return self.visitWhilestmt(ctx.whilestmt())
        elif ctx.forstmt():
            return self.visitForstmt(ctx.forstmt())
        elif ctx.breakstmt():
            return self.visitBreakstmt(ctx.breakstmt())
        elif ctx.contstmt():
            return self.visitContstmt(ctx.contstmt())
        elif ctx.returnstmt():
            return self.visitReturnstmt(ctx.returnstmt())
        elif ctx.exprstmt():
            return self.visitExprstmt(ctx.exprstmt())
        elif ctx.blockstmt():
            return self.visitBlockstmt(ctx.blockstmt())
        
        return None
    
    def visitVardecl(self, ctx:HLangParser.VardeclContext):
        # vardecl: LET ID typeanno ASSIGN expr SEMI ;
        name = ctx.ID().getText()
        type_annotation = None
        if ctx.typeanno():
            type_annotation = self.visitTypeanno(ctx.typeanno())

        value = self.visitExpr(ctx.expr())
        return VarDecl(name, type_annotation, value)
    
    def visitAssignstmt(self, ctx:HLangParser.AssignstmtContext):
        # assignstmt: lvalue ASSIGN expr SEMI ;
        lvalue= self.visitLvalue(ctx.lvalue())
        value = self.visitExpr(ctx.expr())
        return Assignment(lvalue, value)
    
    def visitIfstmt(self, ctx:HLangParser.IfstmtContext):
        # ifstmt: IF LPAREN expr RPAREN blockstmt elselist ;
        condition = self.visitExpr(ctx.expr())
        then_stmt = self.visitBlockstmt(ctx.blockstmt())
        elif_branches = []
        else_stmt = None
        if ctx.elselist():
            elif_branches, else_stmt = self.visitElselist(ctx.elselist())
        return IfStmt(condition, then_stmt, elif_branches, else_stmt)
    
    def visitElselist(self, ctx:HLangParser.ElselistContext):
        # elselist: ELSE IF LPAREN expr RPAREN blockstmt elselist | ELSE blockstmt | ;
        elif_branches = []
        else_stmt = None

        if ctx.ELSE():
            if ctx.IF() and ctx.expr() and ctx.blockstmt():
                elif_condition = self.visitExpr(ctx.expr())
                elif_body = self.visitBlockstmt(ctx.blockstmt())
                elif_branches.append((elif_condition, elif_body))

                if ctx.elselist():
                    remaining_elif,final_else = self.visitElselist(ctx.elselist())
                    elif_branches += remaining_elif
                    if final_else:
                        else_stmt = final_else
                
            elif ctx.blockstmt():
                else_stmt = self.visitBlockstmt(ctx.blockstmt())
        
        return elif_branches, else_stmt
    
    def visitWhilestmt(self, ctx:HLangParser.WhilestmtContext):
        # whilestmt: WHILE LPAREN expr RPAREN blockstmt ;
        condition = self.visitExpr(ctx.expr())
        body = self.visitBlockstmt(ctx.blockstmt())
        return WhileStmt(condition, body)
    
    def visitForstmt(self, ctx:HLangParser.ForstmtContext):
        # forstmt: FOR LPAREN ID IN expr RPAREN blockstmt ;
        variable = ctx.ID().getText()
        iterable = self.visitExpr(ctx.expr())
        body = self.visitBlockstmt(ctx.blockstmt())
        return ForStmt(variable, iterable, body)
    
    def visitBreakstmt(self, ctx:HLangParser.BreakstmtContext):
        # breakstmt: BREAK SEMI ;
        return BreakStmt()

    def visitContstmt(self, ctx: HLangParser.ContstmtContext):
        # contstmt: CONTINUE SEMI ;
        return ContinueStmt()
    
    def visitReturnstmt(self, ctx:HLangParser.ReturnstmtContext):
        # returnstmt: RETURN expropt SEMI ;
        value = None
        if ctx.expropt():
            value = self.visitExpropt(ctx.expropt())
        return ReturnStmt(value)
    
    def visitExpropt(self, ctx: HLangParser.ExproptContext):
        # expropt: expr | ;
        if ctx.expr():
            return self.visitExpr(ctx.expr())
        return None
    
    def visitExprstmt(self, ctx: HLangParser.ExprstmtContext):
        # exprstmt: expr SEMI ;
        expr = self.visitExpr(ctx.expr())
        return ExprStmt(expr)
    
    def visitBlockstmt(self, ctx:HLangParser.BlockstmtContext):
        # blockstmt: LBRACE stmtlist RBRACE ;
        statements = []
        if ctx.stmtlist():
            statements = self.visitStmtlist(ctx.stmtlist())
        return BlockStmt(statements)
    
    # ============= LVALUES =============

    def visitLvalue(self, ctx: HLangParser.LvalueContext):
          # lvalue: ID | arrayaccess | lvalue LBRACK expr RBRACK ;
        if ctx.ID():
            return IdLValue(ctx.ID().getText())
        elif ctx.arrayaccess():
            array_ctx = ctx.arrayaccess()
            array_name = array_ctx.ID().getText()
            base_array = Identifier(array_name) 
            return self.buildArrayAccessLValueFromParts(base_array, array_ctx.accesspart())
        elif ctx.lvalue() and ctx.expr():
            base_lvalue = self.visitLvalue(ctx.lvalue())
            base_expr = self.convertLValueToExpression(base_lvalue)  
            index = self.visitExpr(ctx.expr())
            return ArrayAccessLValue(base_expr, index)
        return None
    
    def convertLValueToExpression(self, lvalue):
        # Convert LValue to Expression
        if isinstance(lvalue, IdLValue):
            return Identifier(lvalue.name)
        elif isinstance(lvalue, ArrayAccessLValue):
            return ArrayAccess(lvalue.array, lvalue.index)
        else:
            return lvalue
    
    def buildArrayAccessLValueFromParts(self, array, accesspart_ctx: HLangParser.AccesspartContext):
          # accesspart: LBRACK expr RBRACK accesspart | LBRACK expr RBRACK ;
        if not accesspart_ctx or not accesspart_ctx.expr():
            return array
        
        index = self.visitExpr(accesspart_ctx.expr())
        
        if accesspart_ctx.accesspart():
            current_access = ArrayAccess(array, index)
            return self.buildArrayAccessLValueFromParts(current_access, accesspart_ctx.accesspart())
        else:
            return ArrayAccessLValue(array, index)
        
    def visitAccesspart(self, ctx:HLangParser.AccesspartContext):
        # accesspart: LBRACK expr RBRACK accesspart | LBRACK expr RBRACK ;
        if ctx.expr():
            return self.visitExpr(ctx.expr())
        return None
    
    # ============= EXPRESSIONS =============
    def visitExpr(self, ctx:HLangParser.ExprContext):
        # expr: pipeexpr ;
        return self.visitPipeexpr(ctx.pipeexpr())
    
    def visitPipeexpr(self,ctx: HLangParser.PipeexprContext):
        # pipeexpr: orexpr pipepart ;
        left =self.visitOrexpr(ctx.orexpr())

        if ctx.pipepart():
            return self.buildPipelineFromParts(left, ctx.pipepart())
        return left

    def buildPipelineFromParts(self,left_expr, pipepart_ctx:HLangParser.PipepartContext):
        # pipepart: PIPE pipecall pipepart | ;
        if not pipepart_ctx or not pipepart_ctx.pipecall():
            return left_expr

        pipecall = self.visitPipecall(pipepart_ctx.pipecall())
        current_pipeline = BinaryOp(left_expr,">>", pipecall)

        if pipepart_ctx.pipepart():
            return self.buildPipelineFromParts(current_pipeline, pipepart_ctx.pipepart())
        return current_pipeline
    
    def visitPipecall(self, ctx :HLangParser.PipecallContext):
        # pipecall: func_id | func_id LPAREN exprlist RPAREN ;
        func_name = self.visitFunc_id(ctx.func_id())  
        if ctx.exprlist():
            args = self.visitExprlist(ctx.exprlist())
            return FunctionCall(Identifier(func_name), args)
        else:
            return Identifier(func_name)
    
    def visitFuncall(self, ctx:HLangParser.FuncallContext):
        # funcall: func_id LPAREN exprlist RPAREN ;
        function_name = self.visitFunc_id(ctx.func_id())  
        args = []
        if ctx.exprlist():
            args = self.visitExprlist(ctx.exprlist())
        return FunctionCall(Identifier(function_name), args)

    def visitOrexpr(self, ctx: HLangParser.OrexprContext):
    # orexpr: andexpr orpart ;
        left = self.visitAndexpr(ctx.andexpr())
        
        if ctx.orpart():
            return self.buildOrFromParts(left, ctx.orpart())
        
        return left

    def buildOrFromParts(self, left_expr, orpart_ctx: HLangParser.OrpartContext):
        # orpart: OR andexpr orpart | ;
        if not orpart_ctx or not orpart_ctx.andexpr():
            return left_expr
        
        right = self.visitAndexpr(orpart_ctx.andexpr())
        current_op = BinaryOp(left_expr, "||", right)
        
        if orpart_ctx.orpart():
            return self.buildOrFromParts(current_op, orpart_ctx.orpart())
        
        return current_op

    def visitAndexpr(self, ctx: HLangParser.AndexprContext):
        # andexpr: eqexpr andpart ;
        left = self.visitEqexpr(ctx.eqexpr())
        
        if ctx.andpart():
            return self.buildAndFromParts(left, ctx.andpart())
        
        return left

    def buildAndFromParts(self, left_expr, andpart_ctx: HLangParser.AndpartContext):
        # andpart: AND eqexpr andpart | ;
        if not andpart_ctx or not andpart_ctx.eqexpr():
            return left_expr
        
        right = self.visitEqexpr(andpart_ctx.eqexpr())
        current_op = BinaryOp(left_expr, "&&", right)
        
        if andpart_ctx.andpart():
            return self.buildAndFromParts(current_op, andpart_ctx.andpart())
        
        return current_op

    def visitEqexpr(self, ctx: HLangParser.EqexprContext):
        # eqexpr: relexpr eqpart ;
        left = self.visitRelexpr(ctx.relexpr())
        
        if ctx.eqpart():
            return self.buildEqualityFromParts(left, ctx.eqpart())
        
        return left

    def buildEqualityFromParts(self, left_expr, eqpart_ctx: HLangParser.EqpartContext):
        # eqpart: eqop relexpr eqpart | ;
        if not eqpart_ctx or not eqpart_ctx.eqop():
            return left_expr
        
        operator = self.visitEqop(eqpart_ctx.eqop())
        right = self.visitRelexpr(eqpart_ctx.relexpr())
        current_op = BinaryOp(left_expr, operator, right)
        
        if eqpart_ctx.eqpart():
            return self.buildEqualityFromParts(current_op, eqpart_ctx.eqpart())
        
        return current_op

    def visitEqop(self, ctx: HLangParser.EqopContext):
        # eqop: EQ | NEQ ;
        if ctx.EQ():
            return "=="
        elif ctx.NEQ():
            return "!="

    def visitRelexpr(self, ctx: HLangParser.RelexprContext):
        # relexpr: addexpr relpart ;
        left = self.visitAddexpr(ctx.addexpr())
        
        if ctx.relpart():
            return self.buildRelationalFromParts(left, ctx.relpart())
        
        return left

    def buildRelationalFromParts(self, left_expr, relpart_ctx: HLangParser.RelpartContext):
        # relpart: relop addexpr relpart | ;
        if not relpart_ctx or not relpart_ctx.relop():
            return left_expr
        
        operator = self.visitRelop(relpart_ctx.relop())
        right = self.visitAddexpr(relpart_ctx.addexpr())
        current_op = BinaryOp(left_expr, operator, right)
        
        if relpart_ctx.relpart():
            return self.buildRelationalFromParts(current_op, relpart_ctx.relpart())
        
        return current_op

    def visitRelop(self, ctx: HLangParser.RelopContext):
        # relop: LT | LE | GT | GE ;
        if ctx.LT():
            return "<"
        elif ctx.LE():
            return "<="
        elif ctx.GT():
            return ">"
        elif ctx.GE():
            return ">="

    def visitAddexpr(self, ctx: HLangParser.AddexprContext):
        # addexpr: mulexpr addpart ;
        left = self.visitMulexpr(ctx.mulexpr())
        
        if ctx.addpart():
            return self.buildAdditiveFromParts(left, ctx.addpart())
        
        return left

    def buildAdditiveFromParts(self, left_expr, addpart_ctx: HLangParser.AddpartContext):
        # addpart: addop mulexpr addpart | ;
        if not addpart_ctx or not addpart_ctx.addop():
            return left_expr
        
        operator = self.visitAddop(addpart_ctx.addop())
        right = self.visitMulexpr(addpart_ctx.mulexpr())
        current_op = BinaryOp(left_expr, operator, right)
        
        if addpart_ctx.addpart():
            return self.buildAdditiveFromParts(current_op, addpart_ctx.addpart())
        
        return current_op

    def visitAddop(self, ctx: HLangParser.AddopContext):
        # addop: PLUS | MINUS ;
        if ctx.PLUS():
            return "+"
        elif ctx.MINUS():
            return "-"

    def visitMulexpr(self, ctx: HLangParser.MulexprContext):
        # mulexpr: unaryexpr mulpart ;
        left = self.visitUnaryexpr(ctx.unaryexpr())
        
        if ctx.mulpart():
            return self.buildMultiplicativeFromParts(left, ctx.mulpart())
        
        return left

    def buildMultiplicativeFromParts(self, left_expr, mulpart_ctx: HLangParser.MulpartContext):
        # mulpart: mulop unaryexpr mulpart | ;
        if not mulpart_ctx or not mulpart_ctx.mulop():
            return left_expr
        
        operator = self.visitMulop(mulpart_ctx.mulop())
        right = self.visitUnaryexpr(mulpart_ctx.unaryexpr())
        current_op = BinaryOp(left_expr, operator, right)
        
        if mulpart_ctx.mulpart():
            return self.buildMultiplicativeFromParts(current_op, mulpart_ctx.mulpart())
        
        return current_op

    def visitMulop(self, ctx: HLangParser.MulopContext):
        # mulop: MUL | DIV | MOD ;
        if ctx.MUL():
            return "*"
        elif ctx.DIV():
            return "/"
        elif ctx.MOD():
            return "%"

    def visitUnaryexpr(self, ctx: HLangParser.UnaryexprContext):
        # unaryexpr: unaryop unaryexpr | primaryexpr ;
        if ctx.unaryop():
            operator = self.visitUnaryop(ctx.unaryop())
            operand = self.visitUnaryexpr(ctx.unaryexpr())
            return UnaryOp(operator, operand)
        elif ctx.primaryexpr():
            return self.visitPrimaryexpr(ctx.primaryexpr())

    def visitUnaryop(self, ctx: HLangParser.UnaryopContext):
        # unaryop: NOT | PLUS | MINUS ;
        if ctx.NOT():
            return "!"
        elif ctx.PLUS():
            return "+"
        elif ctx.MINUS():
            return "-"

    def visitPrimaryexpr(self, ctx: HLangParser.PrimaryexprContext):
        # primaryexpr: literal | arrayaccess | funcall | ID | arraylit | subexpr ;
        if ctx.literal():
            return self.visitLiteral(ctx.literal())
        elif ctx.arrayaccess():
            return self.visitArrayaccess(ctx.arrayaccess())
        elif ctx.funcall():
            return self.visitFuncall(ctx.funcall())
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.arraylit():
            return self.visitArraylit(ctx.arraylit())
        elif ctx.subexpr():
            return self.visitSubexpr(ctx.subexpr())

    # ============= SPECIFIC EXPRESSIONS =============
    def visitLiteral(self, ctx: HLangParser.LiteralContext):
        # literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE ;
        if ctx.INTLIT():
            # return IntegerLiteral(int(ctx.INTLIT().getText()))
            return IntegerLiteral(ctx.INTLIT().getText())
        elif ctx.FLOATLIT():
            return FloatLiteral(ctx.FLOATLIT().getText())
        elif ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)

    def visitArrayaccess(self, ctx: HLangParser.ArrayaccessContext):
        # arrayaccess: ID accesspart ;
        array_name = ctx.ID().getText()
        base_array = Identifier(array_name)
        
        return self.buildArrayAccessFromAccessPartsExpr(base_array, ctx.accesspart())

    def buildArrayAccessFromAccessPartsExpr(self, array, accesspart_ctx: HLangParser.AccesspartContext):
        # accesspart: LBRACK expr RBRACK accesspart | LBRACK expr RBRACK ;
        if not accesspart_ctx or not accesspart_ctx.expr():
            return array
        
        index = self.visitExpr(accesspart_ctx.expr())
        current_access = ArrayAccess(array, index)

        if accesspart_ctx.accesspart():
            return self.buildArrayAccessFromAccessPartsExpr(current_access, accesspart_ctx.accesspart())
        
        return current_access

    def visitArraylit(self, ctx: HLangParser.ArraylitContext):
        # arraylit: LBRACK exprlist RBRACK ;
        elements = []
        if ctx.exprlist():
            elements = self.visitExprlist(ctx.exprlist())
        return ArrayLiteral(elements)

    def visitSubexpr(self, ctx: HLangParser.SubexprContext):
        # subexpr: LPAREN expr RPAREN ;
        return self.visitExpr(ctx.expr())

    # ============= EXPRESSION LISTS =============
    def visitExprlist(self, ctx: HLangParser.ExprlistContext):
        # exprlist: exprprime | ;
        if ctx.exprprime():
            return self.visitExprprime(ctx.exprprime())
        return []

    def visitExprprime(self, ctx: HLangParser.ExprprimeContext):
        # exprprime: expr COMMA exprprime | expr ;
        expressions = []
        if ctx.expr():
            expressions.append(self.visitExpr(ctx.expr()))
        if ctx.exprprime():
            expressions += self.visitExprprime(ctx.exprprime())
        return expressions
    
    def visitFunc_id(self, ctx: HLangParser.Func_idContext):
        # func_id: ID | INT | FLOAT | BOOL | STRING ;
        if ctx.ID():
            return ctx.ID().getText()
        elif ctx.INT():
            return ctx.INT().getText()  # "int"
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()  # "float" 
        elif ctx.BOOL():
            return ctx.BOOL().getText()  # "bool"
        elif ctx.STRING():
            return ctx.STRING().getText()  # "string"
        return None
            




        




            

    