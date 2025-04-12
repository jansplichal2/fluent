import unittest
from fluent_ast import Boolean, Binary, ExprStmt
from interpreter import Interpreter


class TestLogicOperators(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_and_true_true(self):
        expr = ExprStmt(Binary(Boolean(True), "and", Boolean(True)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertTrue(result)

    def test_and_true_false(self):
        expr = ExprStmt(Binary(Boolean(True), "and", Boolean(False)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertFalse(result)

    def test_or_false_true(self):
        expr = ExprStmt(Binary(Boolean(False), "or", Boolean(True)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertTrue(result)

    def test_or_false_false(self):
        expr = ExprStmt(Binary(Boolean(False), "or", Boolean(False)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertFalse(result)

    def test_not_true(self):
        expr = ExprStmt(Binary(Boolean(True), "and not", Boolean(True)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertFalse(result)

    def test_not_false(self):
        expr = ExprStmt(Binary(Boolean(True), "and not", Boolean(False)))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
