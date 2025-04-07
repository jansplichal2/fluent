import re
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Structural
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()

    # Keywords
    FN = auto()
    LET = auto()
    RETURN = auto()
    MATCH = auto()
    IF = auto()
    ELSE = auto()
    PRINT = auto()

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENT = auto()

    # Operators and punctuation
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    ARROW = auto()
    FAT_ARROW = auto()
    COLON = auto()
    COMMA = auto()
    RANGE = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACK = auto()
    RBRACK = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"<Token {self.type.name} '{self.value}' ({self.line}:{self.column})>"


class Lexer:
    KEYWORDS = {
        'fn': TokenType.FN,
        'let': TokenType.LET,
        'return': TokenType.RETURN,
        'match': TokenType.MATCH,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'print': TokenType.PRINT,
    }

    def __init__(self, source: str):
        self.lines = source.splitlines()
        self.line_num = 0
        self.indents = [0]
        self.tokens = []

    def tokenize(self):
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            # Optionally reject tabs:
            if "\t" in line:
                raise SyntaxError(f"Tabs not allowed (line {self.line_num + 1})")
            self._process_line(line)
            self.line_num += 1

        # At end of file, dedent all remaining indent levels.
        while len(self.indents) > 1:
            self.tokens.append(Token(TokenType.DEDENT, '', self.line_num, 0))
            self.indents.pop()

        self.tokens.append(Token(TokenType.EOF, '', self.line_num, 0))
        return self.tokens

    def _process_line(self, line: str):
        if line.strip() == '':
            # Emit a NEWLINE for blank lines (optional)
            self.tokens.append(Token(TokenType.NEWLINE, '', self.line_num, 0))
            return

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Check for unexpected indentation levels (enforce exactly 2-space indents)
        if indent > self.indents[-1]:
            expected = self.indents[-1] + 2
            if indent != expected:
                raise SyntaxError(f"Unexpected indent on line {self.line_num + 1}: expected {expected} spaces, got {indent}")
            self.indents.append(indent)
            self.tokens.append(Token(TokenType.INDENT, '', self.line_num, 0))
        while indent < self.indents[-1]:
            self.indents.pop()
            self.tokens.append(Token(TokenType.DEDENT, '', self.line_num, 0))

        self._tokenize_line(stripped, start_column=(len(line) - len(stripped)))
        self.tokens.append(Token(TokenType.NEWLINE, '', self.line_num, len(line)))

    def _tokenize_line(self, text: str, start_column: int):
        pos = 0
        while pos < len(text):
            current_col = start_column + pos
            if m := re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', text[pos:]):
                word = m.group(0)
                tok_type = self.KEYWORDS.get(word, TokenType.IDENT)
                self.tokens.append(Token(tok_type, word, self.line_num, current_col))
                pos += len(word)
            elif m := re.match(r'\d+', text[pos:]):
                num = m.group(0)
                self.tokens.append(Token(TokenType.NUMBER, num, self.line_num, current_col))
                pos += len(num)
            elif text[pos] == '"':
                end = text.find('"', pos + 1)
                if end == -1:
                    raise SyntaxError(f"Unclosed string starting at line {self.line_num + 1}, column {current_col}")
                value = text[pos + 1:end]
                self.tokens.append(Token(TokenType.STRING, value, self.line_num, current_col))
                pos = end + 1
            elif text[pos:].startswith('->'):
                self.tokens.append(Token(TokenType.ARROW, '->', self.line_num, current_col))
                pos += 2
            elif text[pos:].startswith('=>'):
                self.tokens.append(Token(TokenType.FAT_ARROW, '=>', self.line_num, current_col))
                pos += 2
            elif text[pos:].startswith('..'):
                self.tokens.append(Token(TokenType.RANGE, '..', self.line_num, current_col))
                pos += 2
            elif text[pos] == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line_num, current_col))
                pos += 1
            elif text[pos] == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line_num, current_col))
                pos += 1
            elif text[pos] == '*':
                self.tokens.append(Token(TokenType.STAR, '*', self.line_num, current_col))
                pos += 1
            elif text[pos] == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', self.line_num, current_col))
                pos += 1
            elif text[pos] == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line_num, current_col))
                pos += 1
            elif text[pos] == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line_num, current_col))
                pos += 1
            elif text[pos] == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line_num, current_col))
                pos += 1
            elif text[pos] == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line_num, current_col))
                pos += 1
            elif text[pos] == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line_num, current_col))
                pos += 1
            elif text[pos] == '[':
                self.tokens.append(Token(TokenType.LBRACK, '[', self.line_num, current_col))
                pos += 1
            elif text[pos] == ']':
                self.tokens.append(Token(TokenType.RBRACK, ']', self.line_num, current_col))
                pos += 1
            elif text[pos] in ' \t':
                pos += 1  # skip extra whitespace
            else:
                raise SyntaxError(f"Unexpected character '{text[pos]}' at line {self.line_num + 1}, column {current_col}")


# Example usage:
if __name__ == '__main__':
    source_code = '''
fn fib(n: Int) -> Int
  match n
    0 => 0
    1 => 1
    _ => fib(n - 1) + fib(n - 2)
'''
    lexer = Lexer(source_code)
    for token in lexer.tokenize():
        print(token)
