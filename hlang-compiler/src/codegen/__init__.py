"""
Code Generation Module for HLang Compiler.

This module provides the complete code generation infrastructure for the HLang compiler,
including AST traversal, JVM bytecode generation, and runtime support.

Main Components:
- CodeGen: Main code generator that implements AST visitor pattern
- Emitter: JVM instruction emitter for bytecode generation
- Frame: Method frame management for stack and local variables
- JasminCode: JVM instruction set implementation
- Error handling classes for code generation
- Utility classes for symbol management and I/O operations
"""

# Core code generation components
from .codegen import CodeGenerator
from .emitter import Emitter
from .frame import Frame
from .jasmin_code import JasminCode, MachineCode

# Error handling
from .error import IllegalOperandException, IllegalRuntimeException

# Utility classes
from .utils import FunctionType, Value, Index, CName, Symbol, Access, SubBody

# I/O library support
from .io import LIB_NAME, IO_SYMBOL_LIST

# Main exports for external use
__all__ = [
    # Core code generation
    "CodeGenerator  ",
    "Emitter",
    "Frame",
    "JasminCode",
    "MachineCode",
    # Error handling
    "IllegalOperandException",
    "IllegalRuntimeException",
    # Utility classes
    "FunctionType",
    "Value",
    "Index",
    "CName",
    "Symbol",
    "Access",
    "SubBody",
    # I/O support
    "LIB_NAME",
    "IO_SYMBOL_LIST",
]
