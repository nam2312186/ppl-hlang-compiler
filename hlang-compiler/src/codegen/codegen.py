"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        # Process global constants first and add them to symbol table
        global_symbols = []
        for const_decl in node.const_decls:
            const_symbol = Symbol(const_decl.name, const_decl.type_annotation, CName("HLang"))
            global_symbols.append(const_symbol)
            # Generate static field for global constant
            self.emit.print_out(self.emit.emit_attribute(const_decl.name, const_decl.type_annotation, False, None))

        # Generate static initializer for global constants
        if node.const_decls:
            clinit_frame = Frame("<clinit>", VoidType())
            self.emit.print_out(self.emit.emit_method("<clinit>", FunctionType([], VoidType()), True))
            
            for const_decl in node.const_decls:
                # Generate code to initialize the constant value
                value_code, value_type = self.visit(const_decl.value, Access(clinit_frame, global_symbols + IO_SYMBOL_LIST))
                self.emit.print_out(value_code)
                # Store in static field
                self.emit.print_out(self.emit.emit_put_static(f"HLang/{const_decl.name}", const_decl.type_annotation, clinit_frame))
            
            self.emit.print_out(self.emit.emit_return(VoidType(), clinit_frame))
            self.emit.print_out(self.emit.emit_end_method(clinit_frame))

        # Add global constants to IO_SYMBOL_LIST  
        extended_symbols = global_symbols + IO_SYMBOL_LIST

        # First pass: Create function symbols for all functions to support mutual recursion
        function_symbols = []
        for func_decl in node.func_decls:
            param_types = list(map(lambda x: x.param_type, func_decl.params))
            function_symbol = Symbol(
                func_decl.name,
                FunctionType(param_types, func_decl.return_type),
                CName(self.class_name),
            )
            function_symbols.append(function_symbol)
        
        # Add all function symbols to the environment
        full_symbols = function_symbols + extended_symbols

        # Second pass: Generate method implementations with full symbol table
        for func_decl in node.func_decls:
            frame = Frame(func_decl.name, func_decl.return_type)
            self.generate_method(func_decl, SubBody(frame, full_symbols))

        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))
        
        # Process statements
        for stmt in node.body:
            o = self.visit(stmt, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: SubBody = None):
        if o.frame is None:
            # Global constant - initialization is handled in visit_program's <clinit>
            return SubBody(None, o.sym)
        else:
            # Local constant - treat as immutable local variable
            idx = o.frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    node.name,
                    node.type_annotation,
                    o.frame.get_start_label(),
                    o.frame.get_end_label(),
                )
            )

            # Initialize with the constant value
            value_code, value_type = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(value_code)
            store_code = self.emit.emit_write_var(node.name, node.type_annotation, idx, o.frame)
            self.emit.print_out(store_code)
            
            # Add to symbol table as local constant
            const_symbol = Symbol(node.name, node.type_annotation, Index(idx))
            return SubBody(o.frame, [const_symbol] + o.sym)

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        # Function declaration is now handled in visit_program for mutual recursion
        # This method is kept for compatibility but doesn't generate code
        param_types = list(map(lambda x: x.param_type, node.params))
        function_symbol = Symbol(
            node.name,
            FunctionType(param_types, node.return_type),
            CName(self.class_name),
        )
        
        return SubBody(
            None,
            [function_symbol] + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system

    def visit_int_type(self, node: "IntType", o: Any = None):
        return node

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return node

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        return node

    def visit_string_type(self, node: "StringType", o: Any = None):
        return node

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return node

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        element_type = self.visit(node.element_type, o)
        return ArrayType(element_type, node.dimensions)

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        
        # Type inference: if type_annotation is None, infer from value
        if node.type_annotation is None and node.value is not None:
            # Evaluate the value to get its type
            _, inferred_type = self.visit(node.value, Access(o.frame, o.sym))
            actual_type = inferred_type
        else:
            actual_type = node.type_annotation
            
        if actual_type is None:
            raise Exception(f"Cannot infer type for variable '{node.name}' - no type annotation and no value")
        
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                actual_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        # Create new symbol table with this variable added
        new_sym = [Symbol(node.name, actual_type, Index(idx))] + o.sym
        new_o = SubBody(o.frame, new_sym)
        
        if node.value is not None:
            self.visit(Assignment(IdLValue(node.name), node.value), new_o)
            
        return new_o

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        if isinstance(node.lvalue, ArrayAccessLValue):
            # For array assignment, generate array ref and index first
            # Handle case where array might be a string (variable name)
            if isinstance(node.lvalue.array, str):
                array_node = Identifier(node.lvalue.array)
            else:
                array_node = node.lvalue.array
                
            arr_code, arr_type = self.visit(array_node, Access(o.frame, o.sym))
            self.emit.print_out(arr_code)
            
            idx_code, idx_type = self.visit(node.lvalue.index, Access(o.frame, o.sym))
            self.emit.print_out(idx_code)
            
            # Then generate value
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(rc)
            
            # Finally emit store instruction
            elem_type = arr_type.element_type
            store_code = self.emit.emit_astore(elem_type, o.frame)
            self.emit.print_out(store_code)
        else:
            # For regular assignment - generate value first, then store
            try:
                rc, rt = self.visit(node.value, Access(o.frame, o.sym))
                self.emit.print_out(rc)
            except Exception as e:
                raise e
            
            # Handle identifier assignment
            if isinstance(node.lvalue, IdLValue):
                sym = next(filter(lambda x: x.name == node.lvalue.name, o.sym), None)
                if sym is None:
                    raise Exception(f"Undefined variable: {node.lvalue.name}")
                if type(sym.value) is Index:
                    try:
                        code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
                        self.emit.print_out(code)
                    except Exception as e:
                        raise e
        return o

    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        frame = o.frame
        
        # Simple case: No elif branches
        if not node.elif_branches:
            if node.else_stmt:
                # if-else case
                false_label = frame.get_new_label()
                end_label = frame.get_new_label()
                
                # Handle condition with direct jump for comparison
                if (hasattr(node.condition, 'operator') and 
                    node.condition.operator in ["<", "<=", ">", ">=", "==", "!="]):
                    
                    # Generate left and right operands
                    left_code, left_type = self.visit(node.condition.left, Access(frame, o.sym))
                    right_code, right_type = self.visit(node.condition.right, Access(frame, o.sym))
                    
                    self.emit.print_out(left_code)
                    self.emit.print_out(right_code)
                    
                    # Generate direct conditional jump to false_label
                    op = node.condition.operator
                    if type(left_type) is IntType and type(right_type) is IntType:
                        if op == "<=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGT(false_label))
                        elif op == "<":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGE(false_label))
                        elif op == ">=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLT(false_label))
                        elif op == ">":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLE(false_label))
                        elif op == "==":
                            self.emit.print_out(self.emit.jvm.emitIFICMPNE(false_label))
                        elif op == "!=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(false_label))
                        frame.pop()  # left operand  
                        frame.pop()  # right operand
                    elif type(left_type) is FloatType or type(right_type) is FloatType:
                        # Handle mixed int/float comparisons
                        if type(left_type) is IntType and type(right_type) is FloatType:
                            self.emit.print_out("\ti2f\n")  # Convert left int to float
                        elif type(left_type) is FloatType and type(right_type) is IntType:
                            # Need to handle this differently - convert right operand
                            # Pop right operand, convert, push back
                            frame.pop()  # right operand
                            self.emit.print_out("\ti2f\n")  # Convert top of stack to float
                            frame.push()  # push converted value back
                        
                        # Use fcmpl for float comparison
                        self.emit.print_out(self.emit.jvm.emitFCMPL())
                        frame.pop()  # left operand  
                        frame.pop()  # right operand
                        frame.push()  # fcmpl result
                        
                        if op == "<=":
                            self.emit.print_out(self.emit.jvm.emitIFGT(false_label))
                        elif op == "<":
                            self.emit.print_out(self.emit.jvm.emitIFGE(false_label))
                        elif op == ">=":
                            self.emit.print_out(self.emit.jvm.emitIFLT(false_label))
                        elif op == ">":
                            self.emit.print_out(self.emit.jvm.emitIFLE(false_label))
                        elif op == "==":
                            self.emit.print_out(self.emit.jvm.emitIFNE(false_label))
                        elif op == "!=":
                            self.emit.print_out(self.emit.jvm.emitIFEQ(false_label))
                        frame.pop()  # fcmpl result consumed
                else:
                    # General boolean condition
                    cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
                    self.emit.print_out(cond_code)
                    self.emit.print_out(self.emit.emit_if_false(false_label, frame))
                
                # Generate then statement
                self.visit(node.then_stmt, o)
                
                # Check if then branch ends with return - no need for goto
                needs_goto = True
                if (hasattr(node.then_stmt, 'statements') and 
                    len(node.then_stmt.statements) > 0 and
                    hasattr(node.then_stmt.statements[-1], '__class__') and
                    node.then_stmt.statements[-1].__class__.__name__ == 'ReturnStmt'):
                    needs_goto = False
                
                if needs_goto:
                    # Jump to end after then (skip else)
                    self.emit.print_out(self.emit.emit_goto(end_label, frame))
                
                # Generate else statement 
                self.emit.print_out(self.emit.emit_label(false_label, frame))
                self.visit(node.else_stmt, o)
                
                # End label - only if needed
                if needs_goto:
                    self.emit.print_out(self.emit.emit_label(end_label, frame))
            else:
                # Simple if case
                false_label = frame.get_new_label()
                
                # Handle condition with direct jump for comparison
                if (hasattr(node.condition, 'operator') and 
                    node.condition.operator in ["<", "<=", ">", ">=", "==", "!="]):
                    
                    # Generate left and right operands
                    left_code, left_type = self.visit(node.condition.left, Access(frame, o.sym))
                    right_code, right_type = self.visit(node.condition.right, Access(frame, o.sym))
                    
                    self.emit.print_out(left_code)
                    self.emit.print_out(right_code)
                    
                    # Generate direct conditional jump to false_label
                    op = node.condition.operator
                    if type(left_type) is IntType:
                        if op == "<=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGT(false_label))
                        elif op == "<":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGE(false_label))
                        elif op == ">=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLT(false_label))
                        elif op == ">":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLE(false_label))
                        elif op == "==":
                            self.emit.print_out(self.emit.jvm.emitIFICMPNE(false_label))
                        elif op == "!=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(false_label))
                    
                    frame.pop()  # left operand
                    frame.pop()  # right operand
                else:
                    # General boolean condition
                    cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
                    self.emit.print_out(cond_code)
                    self.emit.print_out(self.emit.emit_if_false(false_label, frame))
                
                # Generate then statement
                self.visit(node.then_stmt, o)
                
                # False label (end of if)
                self.emit.print_out(self.emit.emit_label(false_label, frame))
        else:
            # Complex case with elif branches - use direct jump for all conditions
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            # Handle main condition with direct jump for comparison
            if (hasattr(node.condition, 'operator') and 
                node.condition.operator in ["<", "<=", ">", ">=", "==", "!="]):
                
                # Generate left and right operands
                left_code, left_type = self.visit(node.condition.left, Access(frame, o.sym))
                right_code, right_type = self.visit(node.condition.right, Access(frame, o.sym))
                
                self.emit.print_out(left_code)
                self.emit.print_out(right_code)
                
                # Generate direct conditional jump to false_label
                op = node.condition.operator
                if type(left_type) is IntType:
                    if op == "<=":
                        self.emit.print_out(self.emit.jvm.emitIFICMPGT(false_label))
                    elif op == "<":
                        self.emit.print_out(self.emit.jvm.emitIFICMPGE(false_label))
                    elif op == ">=":
                        self.emit.print_out(self.emit.jvm.emitIFICMPLT(false_label))
                    elif op == ">":
                        self.emit.print_out(self.emit.jvm.emitIFICMPLE(false_label))
                    elif op == "==":
                        self.emit.print_out(self.emit.jvm.emitIFICMPNE(false_label))
                    elif op == "!=":
                        self.emit.print_out(self.emit.jvm.emitIFICMPEQ(false_label))
                
                frame.pop()  # left operand  
                frame.pop()  # right operand
            else:
                # General boolean condition (fallback)
                cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
                self.emit.print_out(cond_code)
                self.emit.print_out(self.emit.emit_if_false(false_label, frame))
            
            # Generate then statement
            self.visit(node.then_stmt, o)
            
            # Check if then branch ends with return - no need for goto
            needs_goto = True
            if (hasattr(node.then_stmt, 'statements') and 
                len(node.then_stmt.statements) > 0 and
                hasattr(node.then_stmt.statements[-1], '__class__') and
                node.then_stmt.statements[-1].__class__.__name__ == 'ReturnStmt'):
                needs_goto = False
            
            if needs_goto:
                # Jump to end if we have elif branches or else clause
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
            
            # Generate elif branches
            current_false_label = false_label
            for elif_condition, elif_block in node.elif_branches:
                # Current false label for previous condition
                self.emit.print_out(self.emit.emit_label(current_false_label, frame))
                
                # New false label for this elif
                current_false_label = frame.get_new_label()
                
                # Handle elif condition with direct jump for comparison
                if (hasattr(elif_condition, 'operator') and 
                    elif_condition.operator in ["<", "<=", ">", ">=", "==", "!="]):
                    
                    # Generate left and right operands
                    left_code, left_type = self.visit(elif_condition.left, Access(frame, o.sym))
                    right_code, right_type = self.visit(elif_condition.right, Access(frame, o.sym))
                    
                    self.emit.print_out(left_code)
                    self.emit.print_out(right_code)
                    
                    # Generate direct conditional jump to current_false_label
                    op = elif_condition.operator
                    if type(left_type) is IntType:
                        if op == "<=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGT(current_false_label))
                        elif op == "<":
                            self.emit.print_out(self.emit.jvm.emitIFICMPGE(current_false_label))
                        elif op == ">=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLT(current_false_label))
                        elif op == ">":
                            self.emit.print_out(self.emit.jvm.emitIFICMPLE(current_false_label))
                        elif op == "==":
                            self.emit.print_out(self.emit.jvm.emitIFICMPNE(current_false_label))
                        elif op == "!=":
                            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(current_false_label))
                    
                    frame.pop()  # left operand  
                    frame.pop()  # right operand
                else:
                    # General boolean condition (fallback)
                    elif_cond_code, elif_cond_type = self.visit(elif_condition, Access(frame, o.sym))
                    self.emit.print_out(elif_cond_code)
                    self.emit.print_out(self.emit.emit_if_false(current_false_label, frame))
                
                # Generate elif block
                self.visit(elif_block, o)
                
                # Check if elif branch ends with return - no need for goto
                elif_needs_goto = True
                if (hasattr(elif_block, 'statements') and 
                    len(elif_block.statements) > 0 and
                    hasattr(elif_block.statements[-1], '__class__') and
                    elif_block.statements[-1].__class__.__name__ == 'ReturnStmt'):
                    elif_needs_goto = False
                
                if elif_needs_goto:
                    # Jump to end
                    self.emit.print_out(self.emit.emit_goto(end_label, frame))
            
            # Generate else statement if exists
            if node.else_stmt:
                self.emit.print_out(self.emit.emit_label(current_false_label, frame))
                self.visit(node.else_stmt, o)
            else:
                # No else clause, just the final false label
                self.emit.print_out(self.emit.emit_label(current_false_label, frame))
            
            # End label
            self.emit.print_out(self.emit.emit_label(end_label, frame))
        
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: SubBody = None):
        frame = o.frame
        
        # Enter loop scope
        frame.enter_loop()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()
        
        # Loop start label
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        
        # Generate condition code
        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        
        # Jump to break_label if condition is false
        self.emit.print_out(self.emit.emit_if_false(break_label, frame))
        
        # Generate loop body
        self.visit(node.body, o)
        
        # Jump back to start
        self.emit.print_out(self.emit.emit_goto(continue_label, frame))
        
        # Break label
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        
        # Exit loop scope
        frame.exit_loop()
        
        return o

    def visit_for_stmt(self, node: "ForStmt", o: SubBody = None):
        # Implement for-in loop according to HLang specification
        # for (variable in collection) { body }
        frame = o.frame
        
        # Generate code for iterable (collection)
        iter_code, iter_type = self.visit(node.iterable, Access(frame, o.sym))
        
        if isinstance(iter_type, ArrayType):
            elem_type = iter_type.element_type
            
            # Enter loop context for break/continue
            frame.enter_loop()
            continue_label = frame.get_continue_label()
            break_label = frame.get_break_label()
            
            # Create loop variable symbol with a local variable index
            var_index = frame.get_new_index()
            loop_var = Symbol(node.variable, elem_type, Index(var_index))
            new_sym = [loop_var] + o.sym
            
            # Get array size and setup variables
            # Load array reference once and store in local variable
            self.emit.print_out(iter_code)
            arr_index = frame.get_new_index()
            self.emit.print_out(self.emit.emit_write_var("_temp_arr", iter_type, arr_index, frame))
            
            # Create index variable 
            index_var = frame.get_new_index()
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))  # Start index = 0
            self.emit.print_out(self.emit.emit_write_var("_index", IntType(), index_var, frame))
            
            # Loop start label
            loop_start = frame.get_new_label()
            self.emit.print_out(self.emit.emit_label(loop_start, frame))
            
            if hasattr(iter_type, 'size') and iter_type.size > 0:
                array_size = iter_type.size
                # For static arrays, use direct size comparison
                # Check condition: index < array_size
                self.emit.print_out(self.emit.emit_read_var("_index", IntType(), index_var, frame))
                self.emit.print_out(self.emit.emit_push_iconst(array_size, frame))
                # if index >= array_size, break
                # Use ificmplt: if index < array_size, continue (skip the break)
                continue_body = frame.get_new_label()
                self.emit.print_out(self.emit.emit_ificmplt(continue_body, frame))  # if index < array_size, continue with body
                self.emit.print_out(self.emit.emit_goto(break_label, frame))       # else break
                self.emit.print_out(self.emit.emit_label(continue_body, frame))
            else:
                # For dynamic arrays (parameters), use arraylength instruction
                # Check condition: index < array.length
                self.emit.print_out(self.emit.emit_read_var("_index", IntType(), index_var, frame))
                self.emit.print_out(self.emit.emit_read_var("_temp_arr", iter_type, arr_index, frame))
                self.emit.print_out(self.emit.emit_arraylength(frame))
                # if index >= array.length, break
                continue_body = frame.get_new_label()
                self.emit.print_out(self.emit.emit_ificmplt(continue_body, frame))  # if index < array.length, continue with body
                self.emit.print_out(self.emit.emit_goto(break_label, frame))       # else break
                self.emit.print_out(self.emit.emit_label(continue_body, frame))
            
            # Load array[index] into loop variable
            # Load array reference
            self.emit.print_out(self.emit.emit_read_var("_temp_arr", iter_type, arr_index, frame))
            # Load index
            self.emit.print_out(self.emit.emit_read_var("_index", IntType(), index_var, frame))
            # Load array element arr[index]
            self.emit.print_out(self.emit.emit_aload(elem_type, frame))
            # Store in loop variable
            self.emit.print_out(self.emit.emit_write_var(node.variable, elem_type, var_index, frame))
            
            # Generate loop body
            self.visit(node.body, SubBody(frame, new_sym))
            
            # Continue label - increment index
            self.emit.print_out(self.emit.emit_label(continue_label, frame))
            self.emit.print_out(self.emit.emit_read_var("_index", IntType(), index_var, frame))
            self.emit.print_out(self.emit.emit_push_iconst(1, frame))
            self.emit.print_out(self.emit.emit_add_op("+", IntType(), frame))
            self.emit.print_out(self.emit.emit_write_var("_index", IntType(), index_var, frame))
            
            # Jump back to loop start
            self.emit.print_out(self.emit.emit_goto(loop_start, frame))
            
            # Break label
            self.emit.print_out(self.emit.emit_label(break_label, frame))
            
            # Exit loop context
            frame.exit_loop()
        else:
            # Just consume the iterable and run body once
            self.emit.print_out(iter_code)
            self.emit.print_out(self.emit.emit_pop(frame))
            self.visit(node.body, o)
        
        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: SubBody = None):
        frame = o.frame
        
        if node.value:
            # Generate code for return value
            value_code, value_type = self.visit(node.value, Access(frame, o.sym))
            self.emit.print_out(value_code)
            
            # Type conversion if needed
            expected_type = frame.return_type
            if type(expected_type) is IntType and type(value_type) is BoolType:
                # Convert boolean to int (boolean values are already 0/1 on JVM stack)
                pass  # No conversion needed as boolean is stored as int
            elif type(expected_type) is FloatType and type(value_type) is IntType:
                # Convert int to float
                self.emit.print_out("\ti2f\n")
                value_type = FloatType()
            elif type(expected_type) is FloatType and type(value_type) is BoolType:
                # Convert boolean to float (via int)
                self.emit.print_out("\ti2f\n") 
                value_type = FloatType()
            
            self.emit.print_out(self.emit.emit_return(expected_type, frame))
        else:
            # Return void
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: SubBody = None):
        frame = o.frame
        break_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_goto(break_label, frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: SubBody = None):
        frame = o.frame
        continue_label = frame.get_continue_label()
        self.emit.print_out(self.emit.emit_goto(continue_label, frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: SubBody = None):
        frame = o.frame
        original_sym = o.sym  # Save original symbol table
        frame.enter_scope(False)
        
        # Emit start label for the block scope
        start_label = frame.get_start_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        
        # Process all statements in the block
        new_o = reduce(lambda acc, cur: self.visit(cur, acc), node.statements, o)
        
        # Emit end label for the block scope
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        
        frame.exit_scope()
        
        # Restore original symbol table but keep frame state
        return SubBody(new_o.frame, original_sym)

    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            False,
        )

        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            return code, sym.type
        
        return "", sym.type

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        # Generate code for array reference
        arr_code, arr_type = self.visit(node.array, o)
        
        # Generate code for index
        idx_code, idx_type = self.visit(node.index, o)
        
        # Generate store instruction based on element type
        elem_type = arr_type.element_type
        # Boolean arrays use integer store instructions in JVM
        store_elem_type = elem_type
        if type(elem_type) is BoolType:
            store_elem_type = IntType()
        store_code = self.emit.emit_astore(store_elem_type, o.frame)
        
        return arr_code + idx_code + store_code, elem_type

    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        frame = o.frame
        
        # Generate code for left operand
        left_code, left_type = self.visit(node.left, o)
        
        # Generate code for right operand  
        right_code, right_type = self.visit(node.right, o)
        
        operator = node.operator
        
        # Arithmetic operations
        if operator in ["+", "-"]:
            # Handle string concatenation first
            if type(left_type) is StringType or type(right_type) is StringType:
                if operator == "+":
                    # String concatenation
                    if type(left_type) is StringType and type(right_type) is StringType:
                        # Both strings - direct concatenation
                        op_code = self.emit.emit_string_concat(frame)
                        result_type = StringType()
                    elif type(left_type) is StringType:
                        # String + non-string: convert right to string
                        if type(right_type) is IntType:
                            right_code += self.emit.emit_invokestatic("io/int2str", IntType(), StringType(), frame)
                        elif type(right_type) is FloatType:
                            right_code += self.emit.emit_invokestatic("io/float2str", FloatType(), StringType(), frame)
                        elif type(right_type) is BoolType:
                            right_code += self.emit.emit_invokestatic("io/bool2str", BoolType(), StringType(), frame)
                        op_code = self.emit.emit_string_concat(frame)
                        result_type = StringType()
                    elif type(right_type) is StringType:
                        # Non-string + string: convert left to string
                        if type(left_type) is IntType:
                            left_code += self.emit.emit_invokestatic("io/int2str", IntType(), StringType(), frame)
                        elif type(left_type) is FloatType:
                            left_code += self.emit.emit_invokestatic("io/float2str", FloatType(), StringType(), frame)
                        elif type(left_type) is BoolType:
                            left_code += self.emit.emit_invokestatic("io/bool2str", BoolType(), StringType(), frame)
                        op_code = self.emit.emit_string_concat(frame)
                        result_type = StringType()
                else:
                    # String subtraction is not allowed
                    raise Exception("String subtraction is not supported")
            # Handle mixed type operations (int + float)
            elif type(left_type) is IntType and type(right_type) is FloatType:
                # Convert int to float
                left_code += "\ti2f\n"
                op_code = self.emit.emit_add_op(operator, FloatType(), frame)
                result_type = FloatType()
            elif type(left_type) is FloatType and type(right_type) is IntType:
                # Convert int to float  
                right_code += "\ti2f\n"
                op_code = self.emit.emit_add_op(operator, FloatType(), frame)
                result_type = FloatType()
            else:
                op_code = self.emit.emit_add_op(operator, left_type, frame)
                result_type = left_type
        elif operator in ["*", "/"]:
            # Handle mixed type operations for multiplication and division
            if type(left_type) is IntType and type(right_type) is FloatType:
                # Convert int to float
                left_code += "\ti2f\n"
                op_code = self.emit.emit_mul_op(operator, FloatType(), frame)
                result_type = FloatType()
            elif type(left_type) is FloatType and type(right_type) is IntType:
                # Convert int to float
                right_code += "\ti2f\n"
                op_code = self.emit.emit_mul_op(operator, FloatType(), frame)
                result_type = FloatType()
            else:
                op_code = self.emit.emit_mul_op(operator, left_type, frame)
                result_type = left_type
        elif operator == "%":
            # Modulo only works with integers
            op_code = self.emit.emit_mod(frame)
            result_type = IntType()
        
        # Comparison operations
        elif operator in ["<", "<=", ">", ">=", "==", "!="]:
            # Handle mixed type comparisons
            if type(left_type) is IntType and type(right_type) is FloatType:
                # Convert int to float for comparison
                left_code += "\ti2f\n"
                op_code = self.emit.emit_re_op(operator, FloatType(), frame)
            elif type(left_type) is FloatType and type(right_type) is IntType:
                # Convert int to float for comparison
                right_code += "\ti2f\n"
                op_code = self.emit.emit_re_op(operator, FloatType(), frame)
            else:
                op_code = self.emit.emit_re_op(operator, left_type, frame)
            result_type = BoolType()
        
        # Logical operations
        elif operator == "&&" or operator == "and":
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            # Short-circuit evaluation
            op_code = (left_code + 
                      self.emit.emit_if_false(false_label, frame) +
                      right_code +
                      self.emit.emit_goto(end_label, frame) +
                      self.emit.emit_label(false_label, frame) +
                      self.emit.emit_push_iconst(0, frame) +
                      self.emit.emit_label(end_label, frame))
            result_type = BoolType()
            
            return op_code, result_type
            
        elif operator == "||" or operator == "or":
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            # Short-circuit evaluation
            op_code = (left_code +
                      self.emit.emit_if_true(true_label, frame) +
                      right_code +
                      self.emit.emit_goto(end_label, frame) +
                      self.emit.emit_label(true_label, frame) +
                      self.emit.emit_push_iconst(1, frame) +
                      self.emit.emit_label(end_label, frame))
            result_type = BoolType()
            
            return op_code, result_type
        
        # Pipeline operator
        elif operator == ">>":
            # Pipeline operator: left >> right => right(left)
            # Get function name from right side
            if hasattr(node.right, 'function'):
                # right is a FunctionCall
                if hasattr(node.right.function, 'name'):
                    function_name = node.right.function.name
                else:
                    function_name = str(node.right.function)
                # Create new FunctionCall with left as first argument
                from src.utils.nodes import FunctionCall
                new_args = [node.left] + (node.right.args if hasattr(node.right, 'args') else [])
                new_call = FunctionCall(node.right.function, new_args)
                return self.visit(new_call, o)
            elif hasattr(node.right, 'name'):
                # right is an Identifier  
                function_name = node.right.name
                from src.utils.nodes import FunctionCall
                new_call = FunctionCall(node.right, [node.left])
                return self.visit(new_call, o)
            else:
                raise Exception(f"Pipeline operator: unsupported right operand type {type(node.right)}")
            
            return op_code, result_type
        
        else:
            raise Exception(f"Unsupported operator: {operator}")
        
        return left_code + right_code + op_code, result_type

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        frame = o.frame
        
        # Generate code for operand
        operand_code, operand_type = self.visit(node.operand, o)
        
        operator = node.operator
        
        if operator == "-":
            op_code = self.emit.emit_neg_op(operand_type, frame)
            result_type = operand_type
        elif operator == "!" or operator == "not":
            # Logical NOT for boolean
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            op_code = (self.emit.emit_if_true(true_label, frame) +
                      self.emit.emit_push_iconst(1, frame) +
                      self.emit.emit_goto(end_label, frame) +
                      self.emit.emit_label(true_label, frame) +
                      self.emit.emit_push_iconst(0, frame) +
                      self.emit.emit_label(end_label, frame))
            result_type = BoolType()
        
        return operand_code + op_code, result_type

    def visit_function_call(self, node: "FunctionCall", o: Access = None):  
        function_name = node.function.name
        # Search for function symbol in symbol table
        function_symbol = None
        for sym in o.sym:
            if hasattr(sym, 'name') and sym.name == function_name:
                function_symbol = sym
                break
        
        # Special handling for len function - generate arraylength bytecode instead of function call
        if function_name == "len":
            if len(node.args) != 1:
                raise Exception(f"len function expects exactly 1 argument, got {len(node.args)}")
            
            # Generate code for the array/string argument
            arg_code, arg_type = self.visit(node.args[0], Access(o.frame, o.sym))
            
            # For arrays, use arraylength instruction
            if isinstance(arg_type, ArrayType):
                return arg_code + self.emit.emit_arraylength(o.frame), IntType()
            # For strings, use String.length() method call
            elif isinstance(arg_type, StringType):
                return arg_code + "\tinvokevirtual java/lang/String/length()I\n", IntType()
            else:
                raise Exception(f"len function not supported for type {type(arg_type)}")
        
        # Generate argument codes and collect types
        argument_codes = []
        arg_types = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes += [ac]
            arg_types.append(at)
        
        if function_symbol is None:
            # Built-in functions are in io class
            if function_name in ["print", "int2str", "float2str", "bool2str", "str2int", "str2float", "input"]:
                class_name = "io"
                # Create function type based on built-in function signatures
                if function_name == "print":
                    func_type = FunctionType(arg_types, VoidType())
                elif function_name in ["int2str", "float2str", "bool2str"]:
                    func_type = FunctionType(arg_types, StringType())
                elif function_name in ["str2int"]:
                    func_type = FunctionType(arg_types, IntType())
                elif function_name in ["str2float"]:
                    func_type = FunctionType(arg_types, FloatType())
                elif function_name == "input":
                    func_type = FunctionType([], StringType())
                else:
                    func_type = FunctionType(arg_types, VoidType())
            else:
                # User-defined functions - try to infer return type from common patterns
                class_name = "HLang"
                
                # Try to infer return type based on function name patterns
                if function_name.startswith("is") or function_name.endswith("Even") or function_name.endswith("Odd"):
                    # Boolean-returning functions
                    func_type = FunctionType(arg_types, BoolType())
                elif function_name in ["half", "double"] or "float" in function_name.lower():
                    # Float-returning functions  
                    func_type = FunctionType(arg_types, FloatType())
                elif function_name in ["factorial", "fibonacci", "sum", "count"] or "int" in function_name.lower():
                    # Integer-returning functions
                    func_type = FunctionType(arg_types, IntType())
                else:
                    # Default to void for unknown functions
                    func_type = FunctionType(arg_types, VoidType())
                    print(f"WARNING: Function '{function_name}' not found in symbol table, inferring return type from name")
        else:
            # Found function symbol - use its type information
            class_name = "HLang"
            if hasattr(function_symbol.value, 'value') and function_symbol.value.value:
                class_name = function_symbol.value.value
            func_type = function_symbol.type

        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, func_type, o.frame
            ),
            func_type.return_type,
        )

    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        # Generate code for array reference
        arr_code, arr_type = self.visit(node.array, o)
        
        # Generate code for index
        idx_code, idx_type = self.visit(node.index, o)
        
        # Generate load instruction based on element type
        elem_type = arr_type.element_type
        # Boolean arrays use integer load instructions in JVM
        if type(elem_type) is BoolType:
            elem_type = IntType()
        load_code = self.emit.emit_aload(elem_type, o.frame)
        
        return arr_code + idx_code + load_code, elem_type

    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None):
        frame = o.frame
        
        # Determine array type from first element or context
        if node.elements:
            first_elem_code, first_elem_type = self.visit(node.elements[0], o)
            elem_type = first_elem_type
        else:
            # Empty array, need type inference from context
            elem_type = IntType()  # Default to int
        
        # Create array
        array_size = len(node.elements)
        
        # Handle nested arrays (arrays of arrays)
        if isinstance(elem_type, ArrayType):
            # For arrays of arrays, we need to create an array of object references
            create_code = (self.emit.emit_push_iconst(array_size, frame) +
                          self.emit.emit_anew_array("[I"))  # Array of int arrays
        elif type(elem_type) is StringType:
            # String arrays are object arrays
            create_code = (self.emit.emit_push_iconst(array_size, frame) +
                          self.emit.emit_anew_array("java/lang/String"))
        else:
            # Determine NEWARRAY type string for primitive arrays
            if type(elem_type) is IntType:
                array_type = "int"
            elif type(elem_type) is BoolType:
                array_type = "int"  # Boolean arrays use int type in JVM
            elif type(elem_type) is FloatType:
                array_type = "float"
            else:
                array_type = "int"  # Default
                
            create_code = (self.emit.emit_push_iconst(array_size, frame) +
                          self.emit.emit_new_array(array_type))
        
        # Initialize elements
        init_code = ""
        for i, elem in enumerate(node.elements):
            elem_code, elem_type_actual = self.visit(elem, o)
            init_code += (self.emit.emit_dup(frame) +
                         self.emit.emit_push_iconst(i, frame) +
                         elem_code)
            
            # Store element based on type
            if isinstance(elem_type_actual, ArrayType) or type(elem_type_actual) is StringType:
                # For nested arrays and strings, use aastore (store object reference)
                init_code += self.emit.emit_aastore(frame)
            else:
                store_type = elem_type_actual
                if type(elem_type_actual) is BoolType:
                    store_type = IntType()
                init_code += self.emit.emit_astore(store_type, frame)
        
        arr_type = ArrayType(elem_type, array_size)
        return create_code + init_code, arr_type

    def visit_identifier(self, node: "Identifier", o: Access = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        
        if sym is None:
            raise Exception(f"Illegal Operand: {node.name}")
        
        if type(sym.value) is Index:
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
        elif type(sym.value) is CName:
            # For global constants, load static field
            if sym.value.value == "HLang":  # Global constant stored as static field
                code = self.emit.emit_get_static(f"HLang/{sym.name}", sym.type, o.frame)
            else:
                # Function or method reference
                code = ""
        
        return code, sym.type

    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None):
        value = 1 if node.value else 0
        return self.emit.emit_push_iconst(value, o.frame), BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return (
            self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame),
            StringType(),
        )
    
    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        # This method is called for ArrayAccessLValue nodes
        # The actual assignment logic is handled in visit_assignment
        return "", VoidType()
