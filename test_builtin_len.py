import unittest
from fluent_ast import Call, String, ExprStmt, Number
from interpreter import Interpreter


class TestBuiltinLen(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_len_on_string(self):
        expr = ExprStmt(Call(func="len", args=[String("abc")]))
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertEqual(result, 3)

    def test_len_type_error(self):
        expr = ExprStmt(Call(func="len", args=[Number(42)]))
        with self.assertRaises(TypeError):
            self.interpreter.eval_stmt(expr, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
