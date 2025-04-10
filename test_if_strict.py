import unittest
from fluent_ast import IfExpr, ExprStmt, Number, String
from interpreter import Interpreter


class TestIfExprStrictTyping(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_if_with_number_condition_raises(self):
        expr = IfExpr(
            condition=Number(1),
            then_branch=[ExprStmt(String("ok"))],
            else_branch=[ExprStmt(String("no"))]
        )
        with self.assertRaises(TypeError):
            self.interpreter.eval_expr(expr, self.interpreter.global_env)

    def test_if_with_string_condition_raises(self):
        expr = IfExpr(
            condition=String("true"),
            then_branch=[ExprStmt(String("ok"))],
            else_branch=[ExprStmt(String("no"))]
        )
        with self.assertRaises(TypeError):
            self.interpreter.eval_expr(expr, self.interpreter.global_env)


if __name__ == '__main__':
    unittest.main()
