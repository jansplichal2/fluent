import unittest
from fluent_ast import ListLiteral, Number, Binary, Var, ExprStmt
from interpreter import Interpreter


class TestListLiterals(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_static_list(self):
        expr = ExprStmt(ListLiteral([Number(1), Number(2), Number(3)]))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertEqual(result, [1, 2, 3])

    def test_expression_list(self):
        self.interpreter.global_env.set("x", 10)
        expr = ExprStmt(ListLiteral([
            Number(1),
            Binary(Number(2), "+", Number(3)),
            Var("x")
        ]))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertEqual(result, [1, 5, 10])


if __name__ == "__main__":
    unittest.main()
