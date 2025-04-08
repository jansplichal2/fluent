from fluent_ast import LetStmt, Number
from lexer import Lexer, TokenType, Token


class Parser:
    def __init__(self, source: str):
        self.tokens = Lexer(source).tokenize()
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.advance()
        if tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok.type} at line {tok.line + 1}")
        return tok

    def parse(self):
        stmts = []
        while self.peek().type != TokenType.EOF:
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tok = self.peek()
        if tok.type == TokenType.LET:
            stmt = self.parse_let()
        else:
            raise SyntaxError(f"Unexpected token: {tok.type} at line {tok.line + 1}")

        # Skip trailing NEWLINE (optional, for single-line forms)
        if self.peek().type == TokenType.NEWLINE:
            self.advance()

        return stmt

    def parse_let(self):
        self.expect(TokenType.LET)
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expr()
        return LetStmt(name=name_tok.value, type_annotation=None, value=value)

    def parse_expr(self):
        tok = self.peek()
        if tok.type == TokenType.NUMBER:
            return self.parse_number()
        else:
            raise SyntaxError(f"Unsupported expression starting with {tok.type}")

    def parse_number(self):
        tok = self.expect(TokenType.NUMBER)
        return Number(value=int(tok.value))


if __name__ == '__main__':
    source = 'let x = 42'
    parser = Parser(source)
    ast = parser.parse()
    for stmt in ast:
        print(stmt)
