from fluent_ast import LetStmt, Number, String, Var, Binary, FnDecl, FnParam, ExprStmt, Call, IfExpr, MatchExpr, MatchCase, Boolean
from lexer import Lexer, TokenType, Token

PRECEDENCE = {
    "or": 1,
    "and": 2,
    "==": 3,
    "!=": 3,
    "<": 3,
    ">": 3,
    "<=": 3,
    ">=": 3,
    "+": 4,
    "-": 4,
    "*": 5,
    "/": 5
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

    def parse_if_expr(self):
        self.expect(TokenType.IF)
        condition = self.parse_expr()

        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)

        then_branch = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            then_branch.append(self.parse_stmt())

        self.expect(TokenType.DEDENT)

        # Parse optional else
        else_branch = None
        if self.peek().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.NEWLINE)
            self.expect(TokenType.INDENT)

            else_branch = []
            while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
                else_branch.append(self.parse_stmt())
            self.expect(TokenType.DEDENT)

        return IfExpr(condition=condition, then_branch=then_branch, else_branch=else_branch)

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

        if tok.type == TokenType.MATCH:
            return self.parse_match_expr()
        elif tok.type == TokenType.IF:
            return self.parse_if_expr()
        elif tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return expr
        elif tok.type == TokenType.NUMBER:
            return self.parse_number()
        elif tok.type == TokenType.STRING:
            return self.parse_string()
        elif tok.type == TokenType.BOOL:
            self.advance()
            return Boolean(tok.value == "true")
        elif tok.type == TokenType.IDENT:
            return self.parse_var()
        else:
            raise SyntaxError(f"Unsupported expression starting with {tok.type}")

    def parse_expr(self, min_precedence=0):
        left = self.parse_unary()

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

            binary_ops = {
                TokenType.PLUS: "+",
                TokenType.MINUS: "-",
                TokenType.STAR: "*",
                TokenType.SLASH: "/",
                TokenType.GT: ">",
                TokenType.LT: "<",
                TokenType.GTE: ">=",
                TokenType.LTE: "<=",
                TokenType.EQ: "==",
                TokenType.NEQ: "!=",
                TokenType.AND: "and",
                TokenType.OR: "or",
            }

            if tok.type in binary_ops:
                op = binary_ops[tok.type]
                precedence = PRECEDENCE[op]
                if precedence < min_precedence:
                    break
                self.advance()
                right = self.parse_expr(precedence + 1)
                left = Binary(left=left, op=op, right=right)
            else:
                break

        return left

    def parse_unary(self):
        tok = self.peek()
        if tok.type == TokenType.NOT:
            self.advance()
            operand = self.parse_unary()
            return Binary(left=Boolean(True), op="and not", right=operand)
        return self.parse_atom()

    def parse_match_expr(self):
        self.expect(TokenType.MATCH)
        matched_expr = self.parse_expr()

        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)

        cases = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            pattern_tok = self.advance()

            if pattern_tok.type == TokenType.UNDERSCORE:
                pattern = "_"
            elif pattern_tok.type == TokenType.NUMBER:
                pattern = int(pattern_tok.value)
            elif pattern_tok.type == TokenType.IDENT:
                pattern = pattern_tok.value
            else:
                raise SyntaxError(f"Invalid match pattern: {pattern_tok.type} on line {pattern_tok.line + 1}")

            self.expect(TokenType.FAT_ARROW)
            expr = self.parse_expr()
            if self.peek().type == TokenType.NEWLINE:
                self.advance()

            cases.append(MatchCase(pattern=pattern, expr=expr))

        self.expect(TokenType.DEDENT)
        return MatchExpr(matched_expr=matched_expr, cases=cases)

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