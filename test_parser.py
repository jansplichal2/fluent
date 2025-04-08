import unittest
from parser import Parser
from fluent_ast import LetStmt, Number, String, Var, Binary, FnDecl, FnParam


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

    def test_fn_simple(self):
        src = '''
fn greet(name: String)
  let msg = "Hi, #{name}"
  msg
'''
        ast = self.parse(src)
        self.assertEqual(len(ast), 1)
        fn = ast[0]
        self.assertIsInstance(fn, FnDecl)
        self.assertEqual(fn.name, "greet")
        self.assertEqual(len(fn.params), 1)
        self.assertEqual(fn.params[0].name, "name")
        self.assertEqual(fn.params[0].type_annotation, "String")
        self.assertEqual(fn.return_type, None)
        self.assertEqual(len(fn.body), 2)
        self.assertIsInstance(fn.body[0], LetStmt)

    def test_fn_with_return_type(self):
        src = '''
fn double(x: Int) -> Int
  x * 2
'''
        fn = self.parse(src)[0]
        self.assertEqual(fn.name, "double")
        self.assertEqual(fn.return_type, "Int")

    def test_fn_multiple_params(self):
        src = '''
fn add(x: Int, y: Int)
  x + y
'''
        fn = self.parse(src)[0]
        self.assertEqual(len(fn.params), 2)
        self.assertEqual(fn.params[1].name, "y")

    def test_fn_missing_paren_error(self):
        src = '''
fn oops(x: Int
  x
'''
        with self.assertRaises(SyntaxError):
            self.parse(src)


if __name__ == "__main__":
    unittest.main()
