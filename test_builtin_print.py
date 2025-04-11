import unittest
from fluent_ast import Call, String, ExprStmt
from interpreter import Interpreter


class TestBuiltInFunctions(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_print_builtin(self):
        expr = ExprStmt(Call(func="print", args=[String("Hello, world!")]))
        # Should not raise; print output goes to stdout
        result = self.interpreter.eval_stmt(expr, self.interpreter.global_env)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
