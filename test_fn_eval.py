import unittest
from fluent_ast import FnDecl, FnParam, LetStmt, Var, Number, Binary, Call, ExprStmt, SimpleType
from interpreter import Interpreter


class TestFunctionEvaluation(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_simple_function_call(self):
        fn = FnDecl(
            name="double",
            params=[FnParam(name="x", type_annotation=SimpleType("Int"))],
            return_type=SimpleType("Int"),
            body=[
                ExprStmt(Binary(Var("x"), "*", Number(2)))
            ]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="double", args=[Number(5)])
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, 10)

    def test_function_with_let(self):
        fn = FnDecl(
            name="sum3",
            params=[
                FnParam("a", SimpleType("Int")),
                FnParam("b", SimpleType("Int")),
                FnParam("c", SimpleType("Int")),
            ],
            return_type=SimpleType("Int"),
            body=[
                LetStmt(name="tmp", type_annotation=None, value=Binary(Var("a"), "+", Var("b"))),
                ExprStmt(Binary(Var("tmp"), "+", Var("c")))
            ]
        )

    def test_call_undefined_function(self):
        call = Call(func="does_not_exist", args=[])
        with self.assertRaises(NameError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)

    def test_call_with_wrong_arg_count(self):
        fn = FnDecl(
            name="add",
            params=[FnParam("x", SimpleType("Int")), FnParam("y", SimpleType("Int"))],
            return_type=SimpleType("Int"),
            body=[ExprStmt(Binary(Var("x"), "+", Var("y")))]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="add", args=[Number(1)])  # only one arg
        with self.assertRaises(ValueError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
