import unittest
from lexer import Lexer, TokenType


def tokens_of(source):
    return [(t.type, t.value) for t in Lexer(source).tokenize() if t.type not in {TokenType.NEWLINE, TokenType.EOF}]


class TestLexer(unittest.TestCase):

    def test_keyword_and_identifier(self):
        source = "fn main"
        tokens = Lexer(source).tokenize()
        filtered = [t for t in tokens if t.type not in {TokenType.NEWLINE, TokenType.EOF}]
        self.assertEqual(filtered[0].line, 0)
        self.assertEqual(filtered[0].column, 0)  # 'fn' starts at column 0
        self.assertEqual(filtered[1].line, 0)
        self.assertEqual(filtered[1].column, 3)  # 'main' starts after "fn "

    def test_number_literal(self):
        source = "let x = 42"
        expected = [
            (TokenType.LET, 'let'),
            (TokenType.IDENT, 'x'),
            (TokenType.ASSIGN, '='),
            (TokenType.NUMBER, '42'),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_string_literal(self):
        source = 'let msg = "hello"'
        expected = [
            (TokenType.LET, 'let'),
            (TokenType.IDENT, 'msg'),
            (TokenType.ASSIGN, '='),
            (TokenType.STRING, 'hello'),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_basic_expression(self):
        source = "a + b * 2"
        expected = [
            (TokenType.IDENT, 'a'),
            (TokenType.PLUS, '+'),
            (TokenType.IDENT, 'b'),
            (TokenType.STAR, '*'),
            (TokenType.NUMBER, '2'),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_function_decl(self):
        source = "fn add(x: Int, y: Int) -> Int"
        expected = [
            (TokenType.FN, 'fn'),
            (TokenType.IDENT, 'add'),
            (TokenType.LPAREN, '('),
            (TokenType.IDENT, 'x'),
            (TokenType.COLON, ':'),
            (TokenType.IDENT, 'Int'),
            (TokenType.COMMA, ','),
            (TokenType.IDENT, 'y'),
            (TokenType.COLON, ':'),
            (TokenType.IDENT, 'Int'),
            (TokenType.RPAREN, ')'),
            (TokenType.ARROW, '->'),
            (TokenType.IDENT, 'Int'),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_match_and_arrows(self):
        source = "match n\n  0 => 1"
        expected = [
            (TokenType.MATCH, 'match'),
            (TokenType.IDENT, 'n'),
            (TokenType.INDENT, ''),
            (TokenType.NUMBER, '0'),
            (TokenType.FAT_ARROW, '=>'),
            (TokenType.NUMBER, '1'),
            (TokenType.DEDENT, ''),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_range_and_lists(self):
        source = "let xs = [0..10]"
        expected = [
            (TokenType.LET, 'let'),
            (TokenType.IDENT, 'xs'),
            (TokenType.ASSIGN, '='),
            (TokenType.LBRACK, '['),
            (TokenType.NUMBER, '0'),
            (TokenType.RANGE, '..'),
            (TokenType.NUMBER, '10'),
            (TokenType.RBRACK, ']'),
        ]
        self.assertEqual(tokens_of(source), expected)

    def test_nested_indents(self):
        source = (
            "fn main\n"
            "  let x = 1\n"
            "  if x\n"
            "    print(x)\n"
            "  let y = 2"
        )
        expected_types = [
            TokenType.FN, TokenType.IDENT,
            TokenType.INDENT,
            TokenType.LET, TokenType.IDENT, TokenType.ASSIGN, TokenType.NUMBER,
            TokenType.IF, TokenType.IDENT,
            TokenType.INDENT,
            TokenType.PRINT, TokenType.LPAREN, TokenType.IDENT, TokenType.RPAREN,
            TokenType.DEDENT,
            TokenType.LET, TokenType.IDENT, TokenType.ASSIGN, TokenType.NUMBER,
            TokenType.DEDENT,
        ]
        result = [t.type for t in Lexer(source).tokenize() if t.type != TokenType.NEWLINE and t.type != TokenType.EOF]
        self.assertEqual(result, expected_types)


class TestLexerErrors(unittest.TestCase):

    def test_unterminated_string(self):
        source = 'let name = "John'
        with self.assertRaises(SyntaxError):
            Lexer(source).tokenize()

    def test_invalid_character(self):
        source = "let x = 42 @"
        with self.assertRaises(SyntaxError):
            Lexer(source).tokenize()

    def test_invalid_operator(self):
        source = "let x = 10 >>> 2"
        with self.assertRaises(SyntaxError):
            Lexer(source).tokenize()

    def test_inconsistent_indentation(self):
        source = (
            "fn test\n"
            "  let a = 1\n"
            "   let b = 2\n"  # too much indent
            "  let c = 3"
        )
        with self.assertRaises(SyntaxError):
            Lexer(source).tokenize()

    def test_tab_vs_space_indent(self):
        source = (
            "fn test\n"
            "\tlet a = 1\n"  # tab indent instead of spaces
        )
        with self.assertRaises(SyntaxError):
            Lexer(source).tokenize()


if __name__ == "__main__":
    unittest.main()
