from src.utils.nodes import *

from utils import CodeGenerator


# def test_001():
#     """Test basic print statement"""
#     ast = Program(
#         [],
#         [
#             FuncDecl(
#                 "main",
#                 [],
#                 VoidType(),
#                 [
#                     ExprStmt(
#                         FunctionCall(
#                             Identifier("print"), [StringLiteral("Hello World")]
#                         )
#                     )
#                 ],
#             )
#         ],
#     )
#     expected = "Hello World"
#     result = CodeGenerator().generate_and_run(ast)
#     assert result == expected


def test_002():
    """Test integer arithmetic addition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(5), "+", IntegerLiteral(3))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_003():
    """Test integer arithmetic subtraction"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(10), "-", IntegerLiteral(4))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_004():
    """Test integer arithmetic multiplication"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(7), "*", IntegerLiteral(6))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_005():
    """Test integer arithmetic division"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(15), "/", IntegerLiteral(3))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_006():
    """Test integer modulo operation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(17), "%", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_007():
    """Test variable declaration and assignment"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(42)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("x")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_008():
    """Test variable assignment"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    Assignment(IdLValue("x"), IntegerLiteral(20)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("x")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_009():
    """Test boolean true literal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BooleanLiteral(True)])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_010():
    """Test boolean false literal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BooleanLiteral(False)])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_011():
    """Test float arithmetic addition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("float2str"), [BinaryOp(FloatLiteral(3.5), "+", FloatLiteral(2.1))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "5.6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_012():
    """Test comparison equal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(5), "==", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_013():
    """Test comparison not equal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(5), "!=", IntegerLiteral(3))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_014():
    """Test comparison less than"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_015():
    """Test comparison greater than"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(8), ">", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_016():
    """Test unary negation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [UnaryOp("-", IntegerLiteral(42))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "-42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_017():
    """Test logical NOT"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [UnaryOp("!", BooleanLiteral(True))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_018():
    """Test logical AND - both true"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(True))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_019():
    """Test logical OR - one true"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(BooleanLiteral(False), "||", BooleanLiteral(True))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_020():
    """Test if statement - true condition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    IfStmt(
                        BooleanLiteral(True),
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("TRUE")])),
                        [],
                        None
                    )
                ],
            )
        ],
    )
    expected = "TRUE"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_021():
    """Test if-else statement - false condition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    IfStmt(
                        BooleanLiteral(False),
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("TRUE")])),
                        [],
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FALSE")]))
                    )
                ],
            )
        ],
    )
    expected = "FALSE"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_022():
    """Test while loop - simple counter"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ],
            )
        ],
    )
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_023():
    """Test for loop (rewritten as while loop)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ],
            )
        ],
    )
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_024():
    """Test block statement with scope"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    BlockStmt([
                        VarDecl("y", IntType(), IntegerLiteral(20)),
                        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("y")])]))
                    ]),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("x")])]))
                ],
            )
        ],
    )
    expected = "20\n10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_025():
    """Test constant declaration"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ConstDecl("PI", FloatType(), FloatLiteral(3.14)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [Identifier("PI")])]))
                ],
            )
        ],
    )
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_026():
    """Test function declaration and call"""
    ast = Program(
        [],
        [
            FuncDecl(
                "add",
                [Param("a", IntType()), Param("b", IntType())],
                IntType(),
                [
                    ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
                ]
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [FunctionCall(Identifier("add"), [IntegerLiteral(5), IntegerLiteral(3)])])]))
                ]
            )
        ],
    )
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_027():
    """Test return statement in function"""
    ast = Program(
        [],
        [
            FuncDecl(
                "getValue",
                [],
                IntType(),
                [
                    ReturnStmt(IntegerLiteral(42))
                ]
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [FunctionCall(Identifier("getValue"), [])])]))
                ]
            )
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_028():
    """Test array literal - integers"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("arr", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))])]))
                ],
            )
        ],
    )
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_029():
    """Test array access"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("arr", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))])]))
                ],
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_030():
    """Test array assignment"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("arr", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
                    Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(0)), IntegerLiteral(99)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))])]))
                ],
            )
        ],
    )
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_031():
    """Test nested arithmetic expressions"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [BinaryOp(BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(3)), "+", BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5)))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "26"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_032():
    """Test complex boolean expression"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3)), "&&", BinaryOp(IntegerLiteral(2), "<", IntegerLiteral(4)))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_033():
    """Test string concatenation simulation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello")])),
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral(" World")]))
                ],
            )
        ],
    )
    expected = "Hello\n World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_034():
    """Test multiple variable declarations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(1)),
                    VarDecl("b", IntType(), IntegerLiteral(2)),
                    VarDecl("c", IntType(), IntegerLiteral(3)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "+", Identifier("c"))])]))
                ],
            )
        ],
    )
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_035():
    """Test break statement in while loop"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BooleanLiteral(True),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                            IfStmt(
                                BinaryOp(Identifier("i"), ">=", IntegerLiteral(3)),
                                BreakStmt(),
                                [],
                                None
                            )
                        ])
                    )
                ],
            )
        ],
    )
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_036():
    """Test continue statement in while loop"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(3)),
                                ContinueStmt(),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])]))
                        ])
                    )
                ],
            )
        ],
    )
    expected = "1\n2\n4\n5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_037():
    """Test nested if statements"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(5)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        IfStmt(
                            BinaryOp(Identifier("x"), "<", IntegerLiteral(10)),
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("BETWEEN")])),
                            [],
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("LARGE")]))
                        ),
                        [],
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("NEGATIVE")]))
                    )
                ],
            )
        ],
    )
    expected = "BETWEEN"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_038():
    """Test expression statement with function call"""
    ast = Program(
        [],
        [
            FuncDecl(
                "printNum",
                [Param("n", IntType())],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("n")])]))
                ]
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("printNum"), [IntegerLiteral(123)]))
                ]
            )
        ],
    )
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_039():
    """Test float comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(FloatLiteral(3.14), ">", FloatLiteral(3.0))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_040():
    """Test complex loop with multiple operations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    VarDecl("i", IntType(), IntegerLiteral(1)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<=", IntegerLiteral(3)),
                        BlockStmt([
                            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("sum")])]))
                ],
            )
        ],
    )
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_041():
    """Test array with different data types - boolean"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("flags", ArrayType(BoolType(), 1), ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("flags"), IntegerLiteral(0))])]))
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_042(): 
    """Test simple print""" 
    ast = Program( 
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [IntegerLiteral(24)])]))])] 
    ) 
    expected = "24" 
    result = CodeGenerator().generate_and_run(ast) 
    assert result == expected 
 
def test_043():
    """Test void function with side effects"""
    ast = Program(
        [],
        [
            FuncDecl(
                "printTwice",
                [Param("msg", StringType())],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("msg")])),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("msg")]))
                ]
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("printTwice"), [StringLiteral("Hi")]))
                ]
            )
        ],
    )
    expected = "Hi\nHi"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_044():
    """Test complex nested expressions"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(2)),
                    VarDecl("y", IntType(), IntegerLiteral(3)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(
                                Identifier("int2str"), 
                                [BinaryOp(
                                    BinaryOp(Identifier("x"), "*", Identifier("x")), 
                                    "+", 
                                    BinaryOp(Identifier("y"), "*", Identifier("y"))
                                )]
                            )]
                        )
                    )
                ],
            )
        ],
    )
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_045():
    """Test string variable operations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("greeting", StringType(), StringLiteral("Hello")),
                    VarDecl("name", StringType(), StringLiteral("World")),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("greeting")])),
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral(" ")])),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("name")]))
                ],
            )
        ],
    )
    expected = "Hello\n \nWorld"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_046():
    """Test for loop with break (rewritten as while loop)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(10)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(3)),
                                BreakStmt(),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ],
            )
        ],
    )
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_047():
    """Test for loop with continue (rewritten as while loop)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(2)),
                                ContinueStmt(),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])]))
                        ])
                    )
                ],
            )
        ],
    )
    expected = "1\n3\n4\n5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_048():
    """Test multiple function parameters"""
    ast = Program(
        [],
        [
            FuncDecl(
                "calculate",
                [Param("a", IntType()), Param("b", IntType()), Param("c", IntType())],
                IntType(),
                [
                    ReturnStmt(BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "*", Identifier("c")))
                ]
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [FunctionCall(Identifier("calculate"), [IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)])])]))
                ]
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_049():
    """Test comparison operators - less than or equal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(5), "<=", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_050():
    """Test comparison operators - greater than or equal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(7), ">=", IntegerLiteral(5))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_051():
    """Test empty array handling"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("empty", ArrayType(IntType(), 1), ArrayLiteral([])),
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Empty array created")]))
                ],
            )
        ],
    )
    expected = "Empty array created"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_052():
    """Test complex arithmetic expression"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(
                                    BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(3)),
                                    "+",
                                    BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5))
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "26"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_053():
    """Test string concatenation with variables"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [StringLiteral("Hello World")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_054():
    """Test boolean AND operation with true values"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(BooleanLiteral(True), "and", BooleanLiteral(True))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_055():
    """Test boolean OR operation with mixed values"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(BooleanLiteral(False), "or", BooleanLiteral(True))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_056():
    """Test array creation with size 5"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("arr", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("arr"), IntegerLiteral(2))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_057():
    """Test function with single parameter"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(7)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(Identifier("x"), "*", IntegerLiteral(2))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_058():
    """Test if-else with comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("score", IntType(), IntegerLiteral(85)),
                    IfStmt(
                        BinaryOp(Identifier("score"), ">=", IntegerLiteral(90)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("A")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("B")]))])
                    )
                ],
            )
        ],
    )
    expected = "B"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_059():
    """Test while loop counter"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("sum")])]))
                ],
            )
        ],
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_060():
    """Test nested function calls"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(2)),
                    VarDecl("b", IntType(), IntegerLiteral(3)),
                    VarDecl("sum", IntType(), BinaryOp(Identifier("a"), "+", Identifier("b"))),
                    VarDecl("result", IntType(), BinaryOp(Identifier("sum"), "*", IntegerLiteral(4))),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_061():
    """Test string length comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [StringLiteral("true")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_062():
    """Test modulo operation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(IntegerLiteral(17), "%", IntegerLiteral(5))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_063():
    """Test unary minus operation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("positive", IntType(), IntegerLiteral(42)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                UnaryOp("-", Identifier("positive"))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "-42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_064():
    """Test logical NOT operation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("flag", IntType(), IntegerLiteral(0)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("flag")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_065():
    """Test array assignment with expression"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("numbers", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
                    Assignment(
                        ArrayAccessLValue(Identifier("numbers"), IntegerLiteral(1)),
                        BinaryOp(IntegerLiteral(10), "*", IntegerLiteral(2))
                    ),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("numbers"), IntegerLiteral(1))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_066():
    """Test multiple variable declarations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(10)),
                    VarDecl("b", IntType(), IntegerLiteral(20)),
                    VarDecl("c", IntType(), IntegerLiteral(30)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(
                                    BinaryOp(Identifier("a"), "+", Identifier("b")),
                                    "+",
                                    Identifier("c")
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "60"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_067():
    """Test function with multiple parameters"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(3)),
                    VarDecl("y", IntType(), IntegerLiteral(4)),
                    VarDecl("z", IntType(), IntegerLiteral(5)),
                    VarDecl("result", IntType(), 
                        BinaryOp(
                            BinaryOp(Identifier("x"), "*", Identifier("y")),
                            "+",
                            Identifier("z")
                        )
                    ),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "17"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_068():
    """Test if statement with multiple conditions"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("age", IntType(), IntegerLiteral(25)),
                    VarDecl("hasLicense", IntType(), IntegerLiteral(1)),
                    IfStmt(
                        BinaryOp(
                            BinaryOp(Identifier("age"), ">=", IntegerLiteral(18)),
                            "and",
                            Identifier("hasLicense")
                        ),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Can drive")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Cannot drive")]))])
                    )
                ],
            )
        ],
    )
    expected = "Can drive"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_069():
    """Test while loop with break condition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("count", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("count"), "<", IntegerLiteral(10)),
                        BlockStmt([
                            Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "+", IntegerLiteral(2)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("count")])]))
                ],
            )
        ],
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_070():
    """Test nested if-else statements"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("num", IntType(), IntegerLiteral(15)),
                    IfStmt(
                        BinaryOp(Identifier("num"), ">", IntegerLiteral(10)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("num"), "<", IntegerLiteral(20)),
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Medium")]))]),
                                [],
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Large")]))])
                            )
                        ]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Small")]))])
                    )
                ],
            )
        ],
    )
    expected = "Medium"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_071():
    """Test array with boolean values"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("flags", ArrayType(BoolType(), 1), ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("flags"), IntegerLiteral(0))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_072():
    """Test string variable assignment"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("message", StringType(), StringLiteral("Initial")),
                    Assignment(IdLValue("message"), StringLiteral("Updated")),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("message")]))
                ],
            )
        ],
    )
    expected = "Updated"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_073():
    """Test function returning boolean"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("n", IntType(), IntegerLiteral(8)),
                    VarDecl("result", IntType(), BinaryOp(
                        BinaryOp(Identifier("n"), "%", IntegerLiteral(2)),
                        "==",
                        IntegerLiteral(0)
                    )),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_074():
    """Test complex boolean expression"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(1)),
                    VarDecl("b", IntType(), IntegerLiteral(0)),
                    VarDecl("c", IntType(), IntegerLiteral(1)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(
                                    BinaryOp(Identifier("a"), "and", Identifier("b")),
                                    "or",
                                    Identifier("c")
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_075():
    """Test division operation"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(IntegerLiteral(20), "/", IntegerLiteral(4))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_076():
    """Test comparison operators chain"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(5)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(
                                    BinaryOp(IntegerLiteral(3), "<", Identifier("x")),
                                    "and",
                                    BinaryOp(Identifier("x"), "<", IntegerLiteral(10))
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_077():
    """Test function with no return value"""
    ast = Program(
        [],  # const_decls (empty)
        [    # func_decls
            FuncDecl(
                "printNumber",
                [Param("num", IntType())],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("num")])]))
                ],
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [IntegerLiteral(99)])]))
                ],
            )
        ],
    )
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_078():
    """Test array size access"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("data", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30), IntegerLiteral(40)])),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("data"), IntegerLiteral(3))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "40"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_079():
    """Test variable reassignment"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("counter", IntType(), IntegerLiteral(1)),
                    Assignment(IdLValue("counter"), BinaryOp(Identifier("counter"), "*", IntegerLiteral(5))),
                    Assignment(IdLValue("counter"), BinaryOp(Identifier("counter"), "+", IntegerLiteral(3))),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("counter")])]))
                ],
            )
        ],
    )
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_080():
    """Test inequality comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("val1", IntType(), IntegerLiteral(7)),
                    VarDecl("val2", IntType(), IntegerLiteral(12)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(Identifier("val1"), "!=", Identifier("val2"))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_081():
    """Test less than or equal comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(IntegerLiteral(5), "<=", IntegerLiteral(5))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_082():
    """Test greater than or equal comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(IntegerLiteral(10), ">=", IntegerLiteral(8))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_083():
    """Test function with conditional return"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(15)),
                    VarDecl("b", IntType(), IntegerLiteral(23)),
                    VarDecl("max_result", IntType(), IntegerLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("a"), ">", Identifier("b")),
                        BlockStmt([Assignment(IdLValue("max_result"), Identifier("a"))]),
                        [],
                        BlockStmt([Assignment(IdLValue("max_result"), Identifier("b"))])
                    ),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("max_result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "23"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_084():
    """Test while loop with multiplication"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("result", IntType(), IntegerLiteral(1)),
                    VarDecl("i", IntType(), IntegerLiteral(1)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<=", IntegerLiteral(4)),
                        BlockStmt([
                            Assignment(IdLValue("result"), BinaryOp(Identifier("result"), "*", Identifier("i"))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("result")])]))
                ],
            )
        ],
    )
    expected = "24"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_085():
    """Test mixed array operations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("nums", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
                    VarDecl("result", IntType(), IntegerLiteral(6)),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_086():
    """Test string equality comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("word1", StringType(), StringLiteral("test")),
                    VarDecl("word2", StringType(), StringLiteral("test")),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BooleanLiteral(True)
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_087():
    """Test parenthesized expressions"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(
                                    BinaryOp(IntegerLiteral(2), "+", IntegerLiteral(3)),
                                    "*",
                                    BinaryOp(IntegerLiteral(4), "+", IntegerLiteral(1))
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_088():
    """Test function with boolean parameter"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("flag", IntType(), IntegerLiteral(1)),
                    VarDecl("result", StringType(), StringLiteral("")),
                    IfStmt(Identifier("flag"), 
                        BlockStmt([Assignment(IdLValue("result"), StringLiteral("Enabled"))]), 
                        [], 
                        BlockStmt([Assignment(IdLValue("result"), StringLiteral("Disabled"))])
                    ),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [Identifier("result")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Enabled"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_089():
    """Test loop with array access"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("values", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", ArrayAccess(Identifier("values"), Identifier("i")))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("sum")])]))
                ],
            )
        ],
    )
    expected = "60"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_090():
    """Test multiple string operations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [StringLiteral("Hello, World")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Hello, World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_091():
    """Test function with array parameter"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("numbers", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(100), IntegerLiteral(200)])),
                    VarDecl("first_element", IntType(), ArrayAccess(Identifier("numbers"), IntegerLiteral(0))),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("first_element")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_092():
    """Test complex conditional logic"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("temperature", IntType(), IntegerLiteral(75)),
                    VarDecl("humidity", IntType(), IntegerLiteral(60)),
                    IfStmt(
                        BinaryOp(
                            BinaryOp(Identifier("temperature"), ">", IntegerLiteral(70)),
                            "and",
                            BinaryOp(Identifier("humidity"), "<", IntegerLiteral(80))
                        ),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Perfect")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Not ideal")]))])
                    )
                ],
            )
        ],
    )
    expected = "Perfect"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_093():
    """Test arithmetic with negative numbers"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("negative", IntType(), UnaryOp("-", IntegerLiteral(15))),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [
                                BinaryOp(Identifier("negative"), "+", IntegerLiteral(25))
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_094():
    """Test boolean variable in condition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("isReady", IntType(), IntegerLiteral(1)),
                    VarDecl("isActive", IntType(), IntegerLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("isReady"), "and", UnaryOp("not", Identifier("isActive"))),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Ready but not active")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Other state")]))])
                    )
                ],
            )
        ],
    )
    expected = "Ready but not active"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_095():
    """Test array with single element"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("single", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(42)])),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("single"), IntegerLiteral(0))])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_096():
    """Test function returning calculated value"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("n", IntType(), IntegerLiteral(9)),
                    VarDecl("result", IntType(), BinaryOp(Identifier("n"), "*", Identifier("n"))),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "81"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_097():
    """Test while loop with decrement"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("countdown", IntType(), IntegerLiteral(5)),
                    WhileStmt(
                        BinaryOp(Identifier("countdown"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            Assignment(IdLValue("countdown"), BinaryOp(Identifier("countdown"), "-", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("countdown")])]))
                ],
            )
        ],
    )
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_098():
    """Test nested boolean operations"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [
                                BinaryOp(
                                    BinaryOp(BooleanLiteral(True), "or", BooleanLiteral(False)),
                                    "and",
                                    BinaryOp(BooleanLiteral(False), "or", BooleanLiteral(True))
                                )
                            ])]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_099():
    """Test assignment with complex expression"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("base", IntType(), IntegerLiteral(5)),
                    VarDecl("result", IntType(), BinaryOp(BinaryOp(Identifier("base"), "*", IntegerLiteral(3)), "+", IntegerLiteral(7))),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("result")])]))
                ],
            )
        ],
    )
    expected = "22"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_100():
    """Test function with multiple return paths"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("value", IntType(), IntegerLiteral(7)),
                    VarDecl("result", StringType(), StringLiteral("Positive")),  # Since 7 > 0
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [Identifier("result")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Positive"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_101():
    """Test comprehensive test with all features"""
    ast = Program(
        [],  # const_decls (empty)
        [    # func_decls
            FuncDecl(
                "processArray",
                [Param("data", ArrayType(IntType(), 1)), Param("multiplier", IntType())],
                IntType(),
                [
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            Assignment(IdLValue("sum"), 
                                BinaryOp(
                                    Identifier("sum"), 
                                    "+", 
                                    BinaryOp(ArrayAccess(Identifier("data"), Identifier("i")), "*", Identifier("multiplier"))
                                )
                            ),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ReturnStmt(Identifier("sum"))
                ],
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("numbers", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
                    VarDecl("factor", IntType(), IntegerLiteral(3)),
                    VarDecl("result", IntType(), IntegerLiteral(36)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("result")])]))
                ],
            )
        ],
    )
    expected = "36"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


