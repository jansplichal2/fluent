import unittest
from fluent_ast import ListLiteral, Number, IndexExpr, ExprStmt, Var
from interpreter import Interpreter


class TestListIndexing(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_index_literal_list(self):
        expr = ExprStmt(IndexExpr(
            target=ListLiteral([Number(10), Number(20), Number(30)]),
            index=Number(1)
        ))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertEqual(result, 20)

    def test_index_variable_list(self):
        self.interpreter.global_env.set("xs", [100, 200, 300])
        expr = ExprStmt(IndexExpr(
            target=Var("xs"),
            index=Number(2)
        ))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertEqual(result, 300)

    def test_index_out_of_bounds(self):
        expr = ExprStmt(IndexExpr(
            target=ListLiteral([Number(1)]),
            index=Number(5)
        ))
        with self.assertRaises(RuntimeError):
            self.interpreter.eval_stmt(expr, self.interpreter.global_env)

    def test_index_not_int(self):
        expr = ExprStmt(IndexExpr(
            target=ListLiteral([Number(1)]),
            index=ListLiteral([])
        ))
        with self.assertRaises(TypeError):
            self.interpreter.eval_stmt(expr, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
