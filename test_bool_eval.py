import unittest
from fluent_ast import Boolean, ExprStmt
from interpreter import Interpreter


class TestBooleanEvaluation(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_true_literal(self):
        expr = ExprStmt(Boolean(True))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertTrue(result)

    def test_false_literal(self):
        expr = ExprStmt(Boolean(False))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
