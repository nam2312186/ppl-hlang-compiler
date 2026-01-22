"""
Visitor interface for AST traversal in HLang programming language.
This module defines the abstract visitor pattern interface for traversing
and processing AST nodes.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .nodes import *


class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""

    def visit(self, node: "ASTNode", o: Any = None):
        return node.accept(self, o)

    # Program and declarations
    @abstractmethod
    def visit_program(self, node: "Program", o: Any = None):
        pass

    @abstractmethod
    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_param(self, node: "Param", o: Any = None):
        pass

    # Type system
    @abstractmethod
    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    @abstractmethod
    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    @abstractmethod
    def visit_bool_type(self, node: "BoolType", o: Any = None):
        pass

    @abstractmethod
    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    @abstractmethod
    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    @abstractmethod
    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    # Statements
    @abstractmethod
    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_assignment(self, node: "Assignment", o: Any = None):
        pass

    @abstractmethod
    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        pass

    # Left-values
    @abstractmethod
    def visit_id_lvalue(self, node: "IdLValue", o: Any = None):
        pass

    @abstractmethod
    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Any = None):
        pass

    # Expressions
    @abstractmethod
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        pass

    @abstractmethod
    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        pass

    @abstractmethod
    def visit_function_call(self, node: "FunctionCall", o: Any = None):
        pass

    @abstractmethod
    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        pass

    @abstractmethod
    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    # Literals
    @abstractmethod
    def visit_integer_literal(self, node: "IntegerLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_boolean_literal(self, node: "BooleanLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        pass
