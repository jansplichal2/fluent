import unittest
from parser import Parser
from fluent_ast import LetStmt, Number, String, Var, Binary, FnDecl, FnParam, Call, IfExpr


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

    def test_simple_function_call(self):
        ast = self.parse('let x = greet("Jan")')
        stmt = ast[0]
        call = stmt.value
        self.assertIsInstance(call, Call)
        self.assertEqual(call.func, "greet")
        self.assertEqual(len(call.args), 1)
        self.assertIsInstance(call.args[0], String)
        self.assertEqual(call.args[0].value, "Jan")

    def test_nested_function_call(self):
        ast = self.parse('let x = log(to_string(42))')
        call = ast[0].value
        self.assertIsInstance(call, Call)
        self.assertEqual(call.func, "log")
        inner = call.args[0]
        self.assertIsInstance(inner, Call)
        self.assertEqual(inner.func, "to_string")
        self.assertEqual(inner.args[0].value, 42)

    def test_function_call_with_expr_arg(self):
        ast = self.parse('let x = add(1 + 2, y)')
        call = ast[0].value
        self.assertIsInstance(call, Call)
        self.assertEqual(len(call.args), 2)
        self.assertIsInstance(call.args[0], Binary)
        self.assertIsInstance(call.args[1], Var)

    def test_call_on_non_var_errors(self):
        with self.assertRaises(SyntaxError):
            self.parse('(1 + 2)(3)')

    def test_if_expression(self):
        src = '''
let result = if x > 0
  "positive"
else
  "non-positive"
'''
        ast = self.parse(src)
        stmt = ast[0]
        self.assertIsInstance(stmt.value, IfExpr)
        self.assertIsInstance(stmt.value.condition, Binary)
        self.assertEqual(len(stmt.value.then_branch), 1)
        self.assertIsInstance(stmt.value.then_branch[0].expr, String)
        self.assertEqual(stmt.value.then_branch[0].expr.value, "positive")

    def test_if_without_else(self):
        src = '''
let result = if ok
  "yes"
'''
        stmt = self.parse(src)[0]
        if_expr = stmt.value
        self.assertIsInstance(if_expr, IfExpr)
        self.assertIsNotNone(if_expr.then_branch)
        self.assertIsNone(if_expr.else_branch)

    def test_nested_else_if(self):
        src = '''
let result = if x > 0
  "positive"
else
  if x < 0
    "negative"
  else
    "zero"
'''
        stmt = self.parse(src)[0]
        if_expr = stmt.value
        self.assertIsInstance(if_expr.else_branch[0].expr, IfExpr)


if __name__ == "__main__":
    unittest.main()
