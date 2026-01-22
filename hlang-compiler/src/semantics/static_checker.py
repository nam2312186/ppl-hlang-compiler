"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from platform import node
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class StaticChecker(ASTVisitor):
    def __init__(self):
        self.global_scope = {}
        self.scope_stack = [{}]
        self.current_function = None
        self.loop_depth = 0
        self.errors = []
        self._declare_builtins()

    def _declare_builtins(self):
        self.global_scope["print"] = {"type": "builtin_print", "kind": "function"}
        self.global_scope["input"] = {"type": "builtin_input", "kind": "function"}
        self.global_scope["int2str"] = {"type": "builtin_int2str", "kind": "function"}
        self.global_scope["float2str"] = {"type": "builtin_float2str", "kind": "function"}
        self.global_scope["bool2str"] = {"type": "builtin_bool2str", "kind": "function"}
        self.global_scope["str2int"] = {"type": "builtin_str2int", "kind": "function"}
        self.global_scope["str2float"] = {"type": "builtin_str2float", "kind": "function"}
        self.global_scope["len"] = {"type": "builtin_len", "kind": "function"}

    def error(self, err):
        if not self.errors:
            self.errors.append(err)

    def enter_scope(self):
        self.scope_stack.append({})

    def exit_scope(self):
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()

    def declare_symbol(self, name, symbol_info):
        current_scope = self.scope_stack[-1]
        if name in current_scope:
            old_kind = current_scope[name]["kind"]
            new_kind = symbol_info["kind"]
            if old_kind == "parameter" and new_kind == "variable":
                self.error(Redeclared("Variable", name))
                return False
            if old_kind == "variable" and new_kind == "parameter":
                self.error(Redeclared("Parameter", name))
                return False
            self.error(Redeclared(new_kind.capitalize(), name))
            return False
        if symbol_info["kind"] in ["constant", "function"]:
            if len(self.scope_stack) > 1:
                self.error(Redeclared(symbol_info["kind"].capitalize(), name))
                return False
        current_scope[name] = symbol_info
        if symbol_info["kind"] in ["function", "constant"]:
            self.global_scope[name] = symbol_info
        return True

    def lookup_symbol(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        if name in self.global_scope:
            return self.global_scope[name]
        return None

    def types_equal(self, t1, t2):
        if type(t1) != type(t2):
            return False
        if isinstance(t1, ArrayType):
            # Arrays with mixed types are never equal to anything
            if hasattr(t1, '_has_mixed_types') or hasattr(t2, '_has_mixed_types'):
                return False
            if t1.element_type is None or t2.element_type is None:
                return False
            try:
                size1_int = int(t1.size)
                size2_int = int(t2.size)
            except Exception:
                return False
            if not isinstance(size1_int, int) or not isinstance(size2_int, int):
                return False
            return self.types_equal(t1.element_type, t2.element_type) and size1_int == size2_int
        return True
        
    def types_compatible(self, expected, actual):
        if self.types_equal(expected, actual):
            return True
        if isinstance(expected, FloatType) and isinstance(actual, IntType):
            return True
        return False

    def _check_all_paths_return(self, stmts):
        found_return = False
        for stmt in stmts:
            if isinstance(stmt, ReturnStmt):
                found_return = True
            elif isinstance(stmt, IfStmt):
                then_returns = self._check_all_paths_return([stmt.then_stmt])
                elif_returns = all(self._check_all_paths_return([elif_stmt]) for _, elif_stmt in getattr(stmt, "elif_branches", []) or [])
                else_returns = self._check_all_paths_return([stmt.else_stmt]) if stmt.else_stmt else False
                if then_returns and elif_returns and else_returns:
                    found_return = True
            elif isinstance(stmt, BlockStmt):
                if self._check_all_paths_return(stmt.statements):
                    found_return = True
        return found_return

    def visit_program(self, node, o=None):
        for const in node.const_decls:
            self.visit(const)
        for func in node.func_decls:
            # Check for redeclaration of built-in functions FIRST
            if func.name in self.global_scope:
                existing = self.global_scope[func.name]
                if (existing["kind"] == "function" and 
                    isinstance(existing["type"], str) and 
                    existing["type"].startswith("builtin_")):
                    self.error(Redeclared("Function", func.name))
                    continue
            
            # Check user function redeclaration
            if func.name in self.global_scope:
                existing = self.global_scope[func.name]
                if (existing["kind"] == "function" and 
                    not (isinstance(existing["type"], str) and existing["type"].startswith("builtin_"))):
                    self.error(Redeclared("Function", func.name))
                    continue
            
            # Create function type and declare
            param_types = [param.param_type for param in func.params]
            func_type = type('FuncType', (), {
                'param_types': param_types,
                'return_type': func.return_type
            })()
            symbol_info = {"type": func_type, "kind": "function", "mutable": False}
            self.global_scope[func.name] = symbol_info
        
        # Then visit function bodies
        for func in node.func_decls:
            self.visit(func)
        
        # Check main function exists
        main = self.lookup_symbol("main")
        if not main or main.get("kind") != "function":
            self.error(NoEntryPoint())
        else:
            main_type = main["type"]
            if isinstance(main_type, str):
                self.error(NoEntryPoint())
            elif not (hasattr(main_type, 'param_types') and len(main_type.param_types) == 0 and isinstance(main_type.return_type, VoidType)):
                self.error(NoEntryPoint())

    def visit_const_decl(self, node, o=None):
        current_scope = self.scope_stack[-1]
        if node.name in current_scope:
            self.error(Redeclared("Constant", node.name))
            return
        
        value_type = self.visit(node.value)
        
        # Check for mixed array literal in const declaration
        if isinstance(value_type, ArrayType) and hasattr(value_type, '_has_mixed_types'):
            self.error(TypeMismatchInStatement(node))
            return
        
        if node.type_annotation:
            if not self.types_equal(node.type_annotation, value_type):
                self.error(TypeMismatchInStatement(node))
            final_type = node.type_annotation
        else:
            final_type = value_type
            if final_type is None:
                self.error(TypeCannotBeInferred(node.value if node.value else node))
                final_type = IntType()
        symbol_info = {"type": final_type, "kind": "constant", "mutable": False}
        self.declare_symbol(node.name, symbol_info)

    def visit_func_decl(self, node, o=None):
        # Check duplicate parameters
        param_names = set()
        for param in node.params:
            if param.name in param_names:
                self.error(Redeclared("Parameter", param.name))
                return
            param_names.add(param.name)
        
        # Enter function scope
        self.enter_scope()
        old_function = self.current_function
        self.current_function = node
        
        # Declare parameters
        for param in node.params:
            param_info = {"type": param.param_type, "kind": "parameter", "mutable": False}
            self.declare_symbol(param.name, param_info)
        
        # Check return paths for non-void functions
        if not isinstance(node.return_type, VoidType):
            has_return = self._check_all_paths_return(node.body)
            if not has_return:
                self.error(TypeMismatchInStatement(node))
        
        # Visit function body
        for stmt in node.body:
            self.visit(stmt)
        
        self.current_function = old_function
        self.exit_scope()

    def visit_param(self, node, o=None):
        return node.param_type

    def visit_var_decl(self, node, o=None):
        current_scope = self.scope_stack[-1]
        if node.name in current_scope:
            self.error(Redeclared("Variable", node.name))
            return
        
        # Handle pipeline and function call checks (existing code unchanged)
        if isinstance(node.value, BinaryOp) and node.value.operator == ">>":
            left_type = self.visit(node.value.left)
            if isinstance(node.value.right, Identifier):
                func_symbol = self.lookup_symbol(node.value.right.name)
                if func_symbol and func_symbol["kind"] == "function":
                    func_type = func_symbol["type"]
                    if hasattr(func_type, "return_type") and isinstance(func_type.return_type, VoidType):
                        self.error(TypeMismatchInStatement(node))  
                        return
            elif isinstance(node.value.right, FunctionCall):
                func_symbol = self.lookup_symbol(node.value.right.function.name)
                if func_symbol and func_symbol["kind"] == "function":
                    func_type = func_symbol["type"]
                    if hasattr(func_type, "return_type") and isinstance(func_type.return_type, VoidType):
                        self.error(TypeMismatchInStatement(node))  
                        return

        if isinstance(node.value, FunctionCall):
            func_symbol = self.lookup_symbol(node.value.function.name)
            if func_symbol:
                func_type = func_symbol["type"]
                if hasattr(func_type, "return_type") and isinstance(func_type.return_type, VoidType):
                    self.error(TypeMismatchInStatement(node))
                    return
        
        # Regular type checking
        value_type = self.visit(node.value, o="var_decl")
        
        # Check for mixed array literal at statement level
        if isinstance(value_type, ArrayType) and hasattr(value_type, '_has_mixed_types'):
            self.error(TypeMismatchInStatement(node))
            return
        
        if isinstance(node.value, ArrayLiteral) and node.type_annotation:
            if len(node.value.elements) == 0:
                self.error(TypeMismatchInStatement(node))
                return
            if len(node.value.elements) != node.type_annotation.size:
                self.error(TypeMismatchInStatement(node))
                return
            for el in node.value.elements:
                el_type = self.visit(el)
                if not self.types_equal(node.type_annotation.element_type, el_type):
                    self.error(TypeMismatchInStatement(node))
                    return
        
        if node.type_annotation:
            if not self.types_equal(node.type_annotation, value_type):
                self.error(TypeMismatchInStatement(node))
            final_type = node.type_annotation
        else:
            final_type = value_type
            if final_type is None or (isinstance(final_type, ArrayType) and final_type.element_type is None):
                self.error(TypeCannotBeInferred(node))
                final_type = IntType()
        
        symbol_info = {"type": final_type, "kind": "variable", "mutable": True}
        self.declare_symbol(node.name, symbol_info)

    def visit_assignment(self, node, o=None):
        # Check void function assignment first (Statement context)
        if isinstance(node.value, FunctionCall):
            func_symbol = self.lookup_symbol(node.value.function.name)
            if func_symbol and hasattr(func_symbol["type"], "return_type"):
                if isinstance(func_symbol["type"].return_type, VoidType):
                    self.error(TypeMismatchInStatement(node))  
                    return
        
        lvalue_type = self.visit(node.lvalue, o=node)  # Pass assignment context
        value_type = self.visit(node.value, o=node)
        
        # Check for mixed array literal in assignment
        if isinstance(value_type, ArrayType) and hasattr(value_type, '_has_mixed_types'):
            self.error(TypeMismatchInStatement(node))
            return
        
        # Check mutability - UPDATED RULES
        if isinstance(node.lvalue, IdLValue):
            symbol = self.lookup_symbol(node.lvalue.name)
            if symbol and not symbol.get("mutable", True):
                self.error(TypeMismatchInStatement(node))
                return
        elif isinstance(node.lvalue, ArrayAccessLValue):
            arr = node.lvalue.array
            while isinstance(arr, (ArrayAccess, ArrayAccessLValue)):
                arr = arr.array
            if isinstance(arr, Identifier):
                symbol = self.lookup_symbol(arr.name)
                if symbol:
                    # Array parameters are now completely immutable (like constants)
                    if symbol["kind"] in ["constant", "parameter"]:
                        self.error(TypeMismatchInStatement(node))
                        return
                    # For loop variables are also immutable
                    elif symbol["kind"] == "variable" and not symbol.get("mutable", True):
                        self.error(TypeMismatchInStatement(node))
                        return
        
        if lvalue_type is None or value_type is None:
            self.error(TypeCannotBeInferred(node))
            return
        if not self.types_equal(lvalue_type, value_type):
            self.error(TypeMismatchInStatement(node))

    def _check_builtin_call_statement(self, node, builtin_type):
        """Check builtin function calls in statement context"""
        if builtin_type == "builtin_int2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, IntType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_float2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, FloatType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_bool2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, BoolType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_str2int":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_str2float":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_len":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, ArrayType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_print":
            if len(node.args) != 1:
                self.error(TypeMismatchInStatement(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInStatement(node))
        elif builtin_type == "builtin_input":
            if len(node.args) != 0:
                self.error(TypeMismatchInStatement(node))

    def visit_if_stmt(self, node, o=None):
        # Simplify condition checking - no error suppression
        cond_type = self.visit(node.condition)
        if not isinstance(cond_type, BoolType):
            self.error(TypeMismatchInStatement(node))
            return
        
        # Visit then branch
        self.enter_scope()
        self.visit(node.then_stmt)
        self.exit_scope()
        
        # Visit elif branches
        if node.elif_branches:
            for elif_cond, elif_stmt in node.elif_branches:
                elif_type = self.visit(elif_cond)
                if not isinstance(elif_type, BoolType):
                    self.error(TypeMismatchInStatement(node))
                    return
                self.enter_scope()
                self.visit(elif_stmt)
                self.exit_scope()
        
        # Visit else branch
        if node.else_stmt:
            self.enter_scope()
            self.visit(node.else_stmt)
            self.exit_scope()

    def visit_while_stmt(self, node, o=None):
        # Check condition type
        cond_type = self.visit(node.condition)
        if not isinstance(cond_type, BoolType):
            self.error(TypeMismatchInStatement(node))
            return
        
        # Enter loop context
        self.loop_depth += 1
        self.enter_scope()
        self.visit(node.body)
        self.exit_scope()
        self.loop_depth -= 1

    def visit_for_stmt(self, node, o=None):
        # Check iterable type first
        iterable_type = self.visit(node.iterable)
        if not isinstance(iterable_type, ArrayType):
            self.error(TypeMismatchInStatement(node))
            return
        
        element_type = iterable_type.element_type
        
        # Enter loop context
        self.loop_depth += 1
        self.enter_scope()
        
        loop_var_info = {"type": element_type, "kind": "variable", "mutable": False}
        current_scope = self.scope_stack[-1]
        current_scope[node.variable] = loop_var_info
        
        if hasattr(node.body, 'statements'):
            # If body is BlockStmt, visit statements directly
            for stmt in node.body.statements:
                self.visit(stmt)
        else:
            # If body is single statement
            self.visit(node.body)
        
        self.exit_scope()
        self.loop_depth -= 1

    def visit_return_stmt(self, node, o=None):
        if not self.current_function:
            return
        expected_type = self.current_function.return_type
        if node.value:
            actual_type = self.visit(node.value)
            if not self.types_equal(expected_type, actual_type):
                self.error(TypeMismatchInStatement(node))
        else:
            if not isinstance(expected_type, VoidType):
                self.error(TypeMismatchInStatement(node))

    def visit_break_stmt(self, node, o=None):
        if self.loop_depth == 0:
            self.error(MustInLoop(node))

    def visit_continue_stmt(self, node, o=None):
        if self.loop_depth == 0:
            self.error(MustInLoop(node))

    def visit_expr_stmt(self, node, o=None):
        if isinstance(node.expr, FunctionCall):
            func_symbol = self.lookup_symbol(node.expr.function.name)
            if not func_symbol:
                self.error(Undeclared(FunctionMarker(), node.expr.function.name))
                return
            
            if func_symbol["kind"] != "function":
                self.error(Undeclared(FunctionMarker(), node.expr.function.name))
                return
            
            # Handle builtin functions
            if isinstance(func_symbol["type"], str):
                self._check_builtin_call_statement(node.expr, func_symbol["type"])
                return
            
            func_type = func_symbol["type"]
            if not hasattr(func_type, 'param_types'):
                self.error(TypeMismatchInStatement(node.expr))
                return
            
            # Check parameter count and types
            if len(node.expr.args) != len(func_type.param_types):
                self.error(TypeMismatchInStatement(node.expr))
                return
            
            for arg, expected_type in zip(node.expr.args, func_type.param_types):
                actual_type = self.visit(arg)
                if not self.types_equal(expected_type, actual_type):
                    self.error(TypeMismatchInStatement(node.expr))
                    return
            
            if not isinstance(func_type.return_type, VoidType):
                self.error(TypeMismatchInStatement(node.expr))
                return
            
            return
        
        # For other expressions, visit normally
        self.visit(node.expr, o="statement")

    def visit_block_stmt(self, node, o=None):
        self.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.exit_scope()

    def visit_int_type(self, node, o=None): return node
    def visit_float_type(self, node, o=None): return node
    def visit_bool_type(self, node, o=None): return node
    def visit_string_type(self, node, o=None): return node
    def visit_void_type(self, node, o=None): return node
    def visit_array_type(self, node, o=None): return node

    def visit_id_lvalue(self, node, o=None):
        symbol = self.lookup_symbol(node.name)
        if not symbol:
            self.error(Undeclared(IdentifierMarker(), node.name))
            return IntType()
        return symbol["type"]

    def visit_array_access_lvalue(self, node, o=None):
        array_type = self.visit(node.array)
        index_type = self.visit(node.index)
        
        # Check for float index in array access (Statement context)
        if not isinstance(index_type, IntType):
            # Check if we're in assignment context
            if o is not None and hasattr(o, '__class__') and o.__class__.__name__ == 'Assignment':
                self.error(TypeMismatchInStatement(o))
            else:
                self.error(TypeMismatchInExpression(node))
            return IntType()
            
        if not isinstance(array_type, ArrayType):
            self.error(TypeMismatchInExpression(node))
            return IntType()
        if array_type.element_type is None:
            self.error(TypeCannotBeInferred(node))
            return IntType()
        return array_type.element_type

    
    def visit_binary_op(self, node, o=None):
        # Handle pipeline operator first
        if node.operator == ">>":
            left_type = self.visit(node.left, o=o)
            if node.right is None or not isinstance(node.right, (Identifier, FunctionCall)):
                self.error(TypeMismatchInExpression(node))
                return IntType()
            
            if isinstance(node.right, Identifier):
                func_symbol = self.lookup_symbol(node.right.name)
                if not func_symbol or func_symbol["kind"] != "function":
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                func_type = func_symbol["type"]
                if isinstance(func_type, str):  
                    self.error(TypeMismatchInExpression(node))  
                    return IntType()
                if not hasattr(func_type, "param_types") or len(func_type.param_types) != 1:
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                if not self.types_equal(func_type.param_types[0], left_type):
                    self.error(TypeMismatchInExpression(node))
                    return func_type.return_type
                return func_type.return_type  
            
            elif isinstance(node.right, FunctionCall):
                func_symbol = self.lookup_symbol(node.right.function.name)
                if not func_symbol or func_symbol["kind"] != "function":
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                func_type = func_symbol["type"]
                if isinstance(func_type, str): 
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                if not hasattr(func_type, "param_types") or len(func_type.param_types) < 1:
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                args_types = [left_type] + [self.visit(arg) for arg in node.right.args]
                if len(args_types) != len(func_type.param_types):
                    self.error(TypeMismatchInExpression(node))
                    return func_type.return_type
                for expected, actual in zip(func_type.param_types, args_types):
                    if not self.types_equal(expected, actual):
                        self.error(TypeMismatchInExpression(node))
                return func_type.return_type 
            else:
                self.error(TypeMismatchInExpression(node))
                return IntType()
        
        # Regular binary operators
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.operator
        
        if isinstance(left_type, VoidType) or isinstance(right_type, VoidType):
            self.error(TypeMismatchInExpression(node))
            return IntType()
        
        if op in ["+", "-", "*", "/", "%"]:
            # Handle string concatenation - anytype + string (except array)
            if op == "+" and isinstance(right_type, StringType):
                # Array + string is still invalid
                if isinstance(left_type, ArrayType):
                    self.error(TypeMismatchInExpression(node))
                    return StringType()
                # Any other type + string is valid
                return StringType()
            
            # Handle string + anytype (except array)  
            if op == "+" and isinstance(left_type, StringType):
                # string + array is still invalid
                if isinstance(right_type, ArrayType):
                    self.error(TypeMismatchInExpression(node))
                    return StringType()
                # string + any other type is valid
                return StringType()
            
            # Regular arithmetic operations (unchanged)
            if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                if op == "%" and not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
                    self.error(TypeMismatchInExpression(node))
                    return IntType()
                if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                    return FloatType()
                return IntType()
            
            # If not string concatenation and not arithmetic, it's an error
            self.error(TypeMismatchInExpression(node))
            return IntType()
        
        elif op in ["<", "<=", ">", ">="]:
            if not (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))):
                self.error(TypeMismatchInExpression(node))
                return BoolType()
            return BoolType()
        
        elif op in ["==", "!="]:
            if isinstance(left_type, ArrayType) or isinstance(right_type, ArrayType):
                self.error(TypeMismatchInExpression(node))
                return BoolType()
            if not self.types_equal(left_type, right_type):
                self.error(TypeMismatchInExpression(node))
            return BoolType()
        
        elif op in ["&&", "||"]:
            if not isinstance(left_type, BoolType) or not isinstance(right_type, BoolType):
                self.error(TypeMismatchInExpression(node))
                return BoolType()
            return BoolType()
        
        else:
            self.error(TypeMismatchInExpression(node))
            return IntType()

    def visit_unary_op(self, node, o=None):
        operand_type = self.visit(node.operand)
        if node.operator in ["+", "-"]:
            if not isinstance(operand_type, (IntType, FloatType)):
                self.error(TypeMismatchInExpression(node))
                return IntType()
            return operand_type
        elif node.operator == "!":
            if not isinstance(operand_type, BoolType):
                self.error(TypeMismatchInExpression(node))
            return BoolType()
        else:
            self.error(TypeMismatchInExpression(node))
            return BoolType()

    def visit_function_call(self, node, o=None):
        func_symbol = self.lookup_symbol(node.function.name)
        if not func_symbol:
            self.error(Undeclared(FunctionMarker(), node.function.name))
            return VoidType()

        # If symbol exists but is NOT a function, it's still undeclared function
        if func_symbol["kind"] != "function":
            self.error(Undeclared(FunctionMarker(), node.function.name))
            return VoidType()
        
        # Handle builtin functions
        if isinstance(func_symbol["type"], str):
            return self._check_builtin_call(node, func_symbol["type"])
        
        func_type = func_symbol["type"]
        if not hasattr(func_type, 'param_types'):
            context = o if o in ["statement", "expression", "var_decl"] else "expression"
            if context == "statement":
                self.error(TypeMismatchInStatement(node))
            else:
                self.error(TypeMismatchInExpression(node))
            return VoidType()
        
        context = o if o in ["statement", "expression", "var_decl"] else "expression"
        
        if len(node.args) != len(func_type.param_types):
            if context == "statement":
                self.error(TypeMismatchInStatement(node))
            else:
                self.error(TypeMismatchInExpression(node))
            return func_type.return_type
        
        for arg, expected_type in zip(node.args, func_type.param_types):
            actual_type = self.visit(arg)
            if not self.types_equal(expected_type, actual_type):
                if context == "statement":
                    self.error(TypeMismatchInStatement(node))
                else:
                    self.error(TypeMismatchInExpression(node))
                return func_type.return_type
        
        return func_type.return_type
        
    def visit_array_access(self, node, o=None):
        array_type = self.visit(node.array)
        index_type = self.visit(node.index)
        if not isinstance(index_type, IntType):
            self.error(TypeMismatchInExpression(node))
            return IntType()
        if not isinstance(array_type, ArrayType):
            self.error(TypeMismatchInExpression(node))
            return IntType()
        if array_type.element_type is None:
            self.error(TypeCannotBeInferred(node))
            return IntType()
        return array_type.element_type

    def visit_identifier(self, node, o=None):
        symbol = self.lookup_symbol(node.name)
        if not symbol:
            self.error(Undeclared(IdentifierMarker(), node.name))
            return IntType()
        return symbol["type"]

    def visit_integer_literal(self, node, o=None): return IntType()
    def visit_float_literal(self, node, o=None): return FloatType()
    def visit_boolean_literal(self, node, o=None): return BoolType()
    def visit_string_literal(self, node, o=None): return StringType()

    def visit_array_literal(self, node, o=None):
        if not node.elements:
            return ArrayType(None, 0)
        
        first_type = self.visit(node.elements[0])
        has_mixed_types = False
        
        for element in node.elements[1:]:
            element_type = self.visit(element)
            if not self.types_equal(first_type, element_type):
                has_mixed_types = True
                break

        if has_mixed_types:
            # Mark the array type as invalid but return it anyway
            array_type = ArrayType(first_type, len(node.elements))
            array_type._has_mixed_types = True  # Add flag to track mixed types
            return array_type
        
        return ArrayType(first_type, len(node.elements))

    def _check_builtin_call(self, node, builtin_type):
        if builtin_type == "builtin_int2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, IntType):
                    self.error(TypeMismatchInExpression(node))
            return StringType()
        elif builtin_type == "builtin_float2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, FloatType):
                    self.error(TypeMismatchInExpression(node))
            return StringType()
        elif builtin_type == "builtin_bool2str":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, BoolType):
                    self.error(TypeMismatchInExpression(node))
            return StringType()
        elif builtin_type == "builtin_str2int":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInExpression(node))
            return IntType()
        elif builtin_type == "builtin_str2float":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInExpression(node))
            return FloatType()
        elif builtin_type == "builtin_len":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, ArrayType):
                    self.error(TypeMismatchInExpression(node))
            return IntType()
        elif builtin_type == "builtin_print":
            if len(node.args) != 1:
                self.error(TypeMismatchInExpression(node))
            else:
                arg_type = self.visit(node.args[0])
                if not isinstance(arg_type, StringType):
                    self.error(TypeMismatchInExpression(node))
            return VoidType()
        elif builtin_type == "builtin_input":
            if len(node.args) != 0:
                self.error(TypeMismatchInExpression(node))
            return StringType()
        return VoidType()

    def visit(self, node, o=None):
        if node is None:
            return None
        return node.accept(self, o)

    def check_program(self, ast):
        self.errors = []
        self.scope_stack = [{}]
        self.current_function = None
        self.loop_depth = 0
        self.global_scope = {}
        self._declare_builtins()
        if ast is None:
            raise Exception("Parse error - AST is None")
        self.visit(ast)
        if self.errors:
            raise Exception(str(self.errors[0]))
        return