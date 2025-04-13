import unittest
from fluent_ast import FnDecl, FnParam, SimpleType, Number, Binary, Var, ExprStmt, Call, Return
from interpreter import Interpreter


class TestFunctionTypeChecking(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_argument_type_ok(self):
        fn = FnDecl(
            name="add",
            params=[FnParam("x", SimpleType("Int")), FnParam("y", SimpleType("Int"))],
            return_type=SimpleType("Int"),
            body=[ExprStmt(Binary(Var("x"), "+", Var("y")))]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="add", args=[Number(1), Number(2)])
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, 3)

    def test_argument_type_mismatch(self):
        fn = FnDecl(
            name="echo",
            params=[FnParam("msg", SimpleType("String"))],
            return_type=SimpleType("String"),
            body=[ExprStmt(Var("msg"))]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="echo", args=[Number(1)])
        with self.assertRaises(TypeError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)

    def test_return_type_ok(self):
        fn = FnDecl(
            name="ten",
            params=[],
            return_type=SimpleType("Int"),
            body=[Return(Number(10))]
        )
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="ten", args=[])
        result = self.interpreter.eval_expr(call, self.interpreter.global_env)
        self.assertEqual(result, 10)

    def test_return_type_mismatch(self):
        fn = FnDecl(
            name="wrong",
            params=[],
            return_type=SimpleType("Int"),
            body=[Return(Var("oops"))]
        )
        self.interpreter.global_env.set("oops", "not an int")
        self.interpreter.eval_stmt(fn, self.interpreter.global_env)
        call = Call(func="wrong", args=[])
        with self.assertRaises(TypeError):
            self.interpreter.eval_expr(call, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
