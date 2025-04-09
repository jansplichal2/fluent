from fluent_ast import LetStmt, Number, String, Var, Binary, FnDecl, FnParam, ExprStmt, Call
from lexer import Lexer, TokenType, Token

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}


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
            # Skip over empty lines
            if self.peek().type == TokenType.NEWLINE:
                self.advance()
                continue
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tok = self.peek()
        if tok.type == TokenType.LET:
            stmt = self.parse_let()
        elif tok.type == TokenType.FN:
            stmt = self.parse_fn_decl()
        else:
            # Fallback: treat it as an expression statement
            expr = self.parse_expr()
            stmt = ExprStmt(expr=expr)

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

    def parse_atom(self):
        tok = self.peek()

        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return expr
        elif tok.type == TokenType.NUMBER:
            return self.parse_number()
        elif tok.type == TokenType.STRING:
            return self.parse_string()
        elif tok.type == TokenType.IDENT:
            return self.parse_var()
        else:
            raise SyntaxError(f"Unsupported expression starting with {tok.type}")

    def parse_expr(self, min_precedence=0):
        left = self.parse_atom()

        while True:
            tok = self.peek()

            # Function call (e.g. foo(1, 2))
            if tok.type == TokenType.LPAREN:
                self.advance()
                args = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.parse_expr())
                    while self.peek().type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expr())
                self.expect(TokenType.RPAREN)
                if isinstance(left, Var):
                    left = Call(func=left.name, args=args)
                else:
                    raise SyntaxError(f"Cannot call non-variable expression at line {tok.line + 1}")
                continue

            # Binary operator
            if tok.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH):
                op = tok.value
                precedence = PRECEDENCE[op]
                if precedence < min_precedence:
                    break

                self.advance()
                right = self.parse_expr(precedence + 1)
                left = Binary(left=left, op=op, right=right)
            else:
                break

        return left

    def parse_number(self):
        tok = self.expect(TokenType.NUMBER)
        return Number(value=int(tok.value))

    def parse_string(self):
        tok = self.expect(TokenType.STRING)
        return String(value=tok.value)

    def parse_var(self):
        tok = self.expect(TokenType.IDENT)
        return Var(name=tok.value)

    def parse_fn_decl(self):
        self.expect(TokenType.FN)
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.LPAREN)
        params = []

        if self.peek().type != TokenType.RPAREN:
            params.append(self.parse_param())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.parse_param())

        self.expect(TokenType.RPAREN)

        return_type = None
        if self.peek().type == TokenType.ARROW:
            self.advance()
            return_type = self.expect(TokenType.IDENT).value

        # Parse block
        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)

        body = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_stmt()
            body.append(stmt)
        self.expect(TokenType.DEDENT)

        return FnDecl(name=name_tok.value, params=params, return_type=return_type, body=body)

    def parse_param(self):
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.COLON)
        type_tok = self.expect(TokenType.IDENT)
        return FnParam(name=name_tok.value, type_annotation=type_tok.value)


if __name__ == '__main__':
    source = 'let x = 42'
    parser = Parser(source)
    ast = parser.parse()
    for stmt in ast:
        print(stmt)

    parser = Parser('5 + 6 + 7 + 8 * 9')
    print(parser.parse_expr())