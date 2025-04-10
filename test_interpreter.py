import unittest
from fluent_ast import LetStmt, Var, Number, String, Binary, ExprStmt
from interpreter import Interpreter, Environment


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_literal_number(self):
        result = self.interpreter.eval_expr(Number(42), self.interpreter.global_env)
        self.assertEqual(result, 42)

    def test_literal_string(self):
        result = self.interpreter.eval_expr(String("hello"), self.interpreter.global_env)
        self.assertEqual(result, "hello")

    def test_binary_addition(self):
        expr = Binary(left=Number(2), op="+", right=Number(3))
        result = self.interpreter.eval_expr(expr, self.interpreter.global_env)
        self.assertEqual(result, 5)

    def test_variable_reference(self):
        env = Environment()
        env.set("x", 10)
        expr = Var("x")
        result = self.interpreter.eval_expr(expr, env)
        self.assertEqual(result, 10)

    def test_let_binding(self):
        stmt = LetStmt(name="x", type_annotation=None, value=Number(100))
        self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        result = self.interpreter.global_env.get("x")
        self.assertEqual(result, 100)

    def test_expr_statement(self):
        stmt = ExprStmt(expr=Binary(Number(1), "+", Number(2)))
        result = self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
