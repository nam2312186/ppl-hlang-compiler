from ..utils.nodes import *
from .utils import *


LIB_NAME = "io"

IO_SYMBOL_LIST = [
    Symbol("print", FunctionType([StringType()], VoidType()), CName(LIB_NAME)),
    Symbol("input", FunctionType([], StringType()), CName(LIB_NAME)),
    Symbol("int2str", FunctionType([IntType()], StringType()), CName(LIB_NAME)),
    Symbol("str2int", FunctionType([StringType()], IntType()), CName(LIB_NAME)),
    Symbol("float2str", FunctionType([FloatType()], StringType()), CName(LIB_NAME)),
    Symbol("str2float", FunctionType([StringType()], FloatType()), CName(LIB_NAME)),
    Symbol("bool2str", FunctionType([BoolType()], StringType()), CName(LIB_NAME)),
]
