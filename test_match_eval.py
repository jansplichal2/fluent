import unittest
from fluent_ast import MatchExpr, MatchCase, Number, String, Var, ExprStmt, IfExpr, Binary
from interpreter import Interpreter


class TestMatchExprEvaluation(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_literal_match(self):
        expr = MatchExpr(
            matched_expr=Number(2),
            cases=[
                MatchCase(pattern=1, expr=String("one")),
                MatchCase(pattern=2, expr=String("two")),
                MatchCase(pattern="_", expr=String("other")),
            ]
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, "two")

    def test_wildcard_fallback(self):
        expr = MatchExpr(
            matched_expr=Number(5),
            cases=[
                MatchCase(pattern=1, expr=String("one")),
                MatchCase(pattern=2, expr=String("two")),
                MatchCase(pattern="_", expr=String("other")),
            ]
        )
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, "other")

    def test_match_with_if_expr_branch(self):
        expr = MatchExpr(
            matched_expr=Number(3),
            cases=[
                MatchCase(pattern=1, expr=String("one")),
                MatchCase(pattern="_", expr=IfExpr(
                    condition=Binary(Var("x"), ">", Number(2)),
                    then_branch=[ExprStmt(String("many"))],
                    else_branch=[ExprStmt(String("few"))]
                )),
            ]
        )
        self.interpreter.global_env.set("x", 3)
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, "many")


if __name__ == "__main__":
    unittest.main()
