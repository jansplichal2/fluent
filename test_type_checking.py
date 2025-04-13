import unittest
from fluent_ast import LetStmt, Number, String as Str, Boolean, ListLiteral, SimpleType, ListType
from interpreter import Interpreter


class TestLetTypeChecking(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_int_assignment_ok(self):
        stmt = LetStmt(name="x", type_annotation=SimpleType("Int"), value=Number(42))
        result = self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        self.assertEqual(result, 42)

    def test_string_assignment_ok(self):
        stmt = LetStmt(name="s", type_annotation=SimpleType("String"), value=Str("hello"))
        result = self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        self.assertEqual(result, "hello")

    def test_bool_assignment_ok(self):
        stmt = LetStmt(name="b", type_annotation=SimpleType("Bool"), value=Boolean(True))
        result = self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        self.assertTrue(result)

    def test_type_mismatch_int_string(self):
        stmt = LetStmt(name="x", type_annotation=SimpleType("Int"), value=Str("oops"))
        with self.assertRaises(TypeError):
            self.interpreter.eval_stmt(stmt, self.interpreter.global_env)

    def test_list_int_ok(self):
        stmt = LetStmt(
            name="xs",
            type_annotation=ListType(SimpleType("Int")),
            value=ListLiteral([Number(1), Number(2)])
        )
        result = self.interpreter.eval_stmt(stmt, self.interpreter.global_env)
        self.assertEqual(result, [1, 2])

    def test_list_string_mismatch(self):
        stmt = LetStmt(
            name="xs",
            type_annotation=ListType(SimpleType("String")),
            value=ListLiteral([Number(1), Number(2)])
        )
        with self.assertRaises(TypeError):
            self.interpreter.eval_stmt(stmt, self.interpreter.global_env)


if __name__ == "__main__":
    unittest.main()
