import unittest
from fluent_ast import FnDecl, FnParam, LetStmt, Var, Number, Binary, Call, ExprStmt
from interpreter import Interpreter


class TestFunctionEvaluation(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_simple_function_call(self):
        fn = FnDecl(
            name="double",
            params=[FnParam(name="x", type_annotation="Int")],
            return_type="Int",
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
            params=[FnParam("a", "Int"), FnParam("b", "Int"), FnParam("c", "Int")],
            return_type="Int",
            body=[
                LetStmt(name="tmp", type_annotation=None, value=Binary(Var("a"), "+", Var("b"))),
                ExprStmt(Binary(Var("tmp"), "+", Var("c")))
            ]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="sum3", args=[Number(1), Number(2), Number(3)])
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, 6)

    def test_call_undefined_function(self):
        call = Call(func="does_not_exist", args=[])
        with self.assertRaises(NameError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)

    def test_call_with_wrong_arg_count(self):
        fn = FnDecl(
            name="add",
            params=[FnParam("x", "Int"), FnParam("y", "Int")],
            return_type="Int",
            body=[ExprStmt(Binary(Var("x"), "+", Var("y")))]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="add", args=[Number(1)])  # only one arg
        with self.assertRaises(ValueError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
