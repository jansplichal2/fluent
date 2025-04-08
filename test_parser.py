import unittest
from parser import Parser
from fluent_ast import LetStmt, Number, String, Var, Binary


class TestParser(unittest.TestCase):

    def parse(self, source):
        return Parser(source).parse()

    def test_let_simple(self):
        ast = self.parse("let x = 42")
        self.assertEqual(len(ast), 1)
        stmt = ast[0]
        self.assertIsInstance(stmt, LetStmt)
        self.assertEqual(stmt.name, "x")
        self.assertIsNone(stmt.type_annotation)
        self.assertIsInstance(stmt.value, Number)
        self.assertEqual(stmt.value.value, 42)

    def test_let_with_type(self):
        # placeholder: once we implement type annotations
        pass

    def test_let_missing_identifier(self):
        with self.assertRaises(SyntaxError):
            self.parse("let = 42")

    def test_let_missing_equals(self):
        with self.assertRaises(SyntaxError):
            self.parse("let x 42")

    def test_multiple_lets(self):
        source = "let a = 1\nlet b = 2"
        ast = self.parse(source)
        self.assertEqual(len(ast), 2)
        self.assertEqual(ast[0].name, "a")
        self.assertEqual(ast[1].name, "b")

    def test_let_string(self):
        ast = self.parse('let name = "Jan"')
        stmt = ast[0]
        self.assertEqual(stmt.name, "name")
        self.assertIsInstance(stmt.value, String)
        self.assertEqual(stmt.value.value, "Jan")

    def test_let_binary_add(self):
        ast = self.parse("let x = 1 + 2")
        expr = ast[0].value
        self.assertIsInstance(expr, Binary)
        self.assertEqual(expr.op, "+")
        self.assertIsInstance(expr.left, Number)
        self.assertIsInstance(expr.right, Number)

    def test_binary_precedence(self):
        ast = self.parse("let x = 1 + 2 * 3")
        expr = ast[0].value
        self.assertIsInstance(expr, Binary)
        self.assertEqual(expr.op, "+")
        self.assertIsInstance(expr.right, Binary)
        self.assertEqual(expr.right.op, "*")

    def test_binary_with_var(self):
        ast = self.parse("let x = y * 10")
        expr = ast[0].value
        self.assertIsInstance(expr.left, Var)
        self.assertIsInstance(expr.right, Number)

    def test_binary_with_parentheses(self):
        ast = self.parse("let x = 1 * (2 + 3)")
        expr = ast[0].value
        self.assertEqual(expr.op, "*")
        self.assertIsInstance(expr.right, Binary)
        self.assertEqual(expr.right.op, "+")


if __name__ == "__main__":
    unittest.main()
