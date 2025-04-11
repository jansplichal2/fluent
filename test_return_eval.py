import unittest
from fluent_ast import FnDecl, FnParam, Return, ExprStmt, String, IfExpr, Binary, Var, Number, Call
from interpreter import Interpreter


class TestReturnStatement(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_function_returns_early(self):
        fn = FnDecl(
            name="early_exit",
            params=[FnParam("x", "Int")],
            return_type="String",
            body=[
                ExprStmt(IfExpr(
                    condition=Binary(Var("x"), ">", Number(0)),
                    then_branch=[Return(String("positive"))],
                    else_branch=None
                )),
                ExprStmt(String("not positive"))
            ]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="early_exit", args=[Number(5)])
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, "positive")

    def test_function_returns_fallback(self):
        fn = FnDecl(
            name="early_exit",
            params=[FnParam("x", "Int")],
            return_type="String",
            body=[
                ExprStmt(
                IfExpr(
                    condition=Binary(Var("x"), ">", Number(0)),
                    then_branch=[Return(String("positive"))],
                    else_branch=None
                )),
                ExprStmt(String("not positive"))
            ]
        )
        call = Call(func="early_exit", args=[Number(-2)])
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, "not positive")


if __name__ == "__main__":
    unittest.main()
