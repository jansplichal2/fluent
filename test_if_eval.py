import unittest
from fluent_ast import IfExpr, LetStmt, String, Number, Var, Binary, ExprStmt
from interpreter import Interpreter


class TestIfExprEvaluation(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_if_then_branch(self):
        expr = IfExpr(
            condition=Number(True),
            then_branch=[ExprStmt(String("yes"))],
            else_branch=[ExprStmt(String("no"))]
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, "yes")

    def test_if_else_branch(self):
        expr = IfExpr(
            condition=Number(False),
            then_branch=[ExprStmt(String("yes"))],
            else_branch=[ExprStmt(String("no"))]
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, "no")

    def test_if_without_else(self):
        expr = IfExpr(
            condition=Number(False),
            then_branch=[ExprStmt(String("yes"))],
            else_branch=None
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertIsNone(result)

    def test_if_with_let_and_expression(self):
        expr = IfExpr(
            condition=Number(True),
            then_branch=[
                LetStmt(name="x", type_annotation=None, value=Number(5)),
                ExprStmt(Binary(Var("x"), "*", Number(2)))
            ],
            else_branch=None
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, 10)


if __name__ == "__main__":
    unittest.main()
