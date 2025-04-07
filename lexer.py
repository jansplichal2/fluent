from enum import Enum, auto
from dataclasses import dataclass
import re


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
        self.current_indent_level = 0

    def tokenize(self):
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            self._process_line(line)
            self.line_num += 1

        # Handle end-of-file dedents
        while len(self.indents) > 1:
            self.tokens.append(Token(TokenType.DEDENT, '', self.line_num, 0))
            self.indents.pop()

        self.tokens.append(Token(TokenType.EOF, '', self.line_num, 0))
        return self.tokens

    def _process_line(self, line: str):
        if line.strip() == '':
            return  # Skip empty lines

        if '\t' in line:
            raise SyntaxError(f"Tabs not allowed (line {self.line_num + 1})")

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent > self.indents[-1]:
            if indent - self.indents[-1] not in {2, 4}:
                raise SyntaxError(
                    f"Inconsistent indentation on line {self.line_num + 1} (got {indent}, expected step of 2 or 4)")
            self.indents.append(indent)
            self.tokens.append(Token(TokenType.INDENT, '', self.line_num, 0))

        while indent < self.indents[-1]:
            self.indents.pop()
            self.tokens.append(Token(TokenType.DEDENT, '', self.line_num, 0))

        self._tokenize_line(stripped)
        self.tokens.append(Token(TokenType.NEWLINE, '', self.line_num, len(line)))

    def _tokenize_line(self, text: str):
        pos = 0
        while pos < len(text):
            if m := re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', text[pos:]):
                word = m.group(0)
                tok_type = self.KEYWORDS.get(word, TokenType.IDENT)
                self.tokens.append(Token(tok_type, word, self.line_num, pos))
                pos += len(word)
            elif m := re.match(r'\d+', text[pos:]):
                num = m.group(0)
                self.tokens.append(Token(TokenType.NUMBER, num, self.line_num, pos))
                pos += len(num)
            elif text[pos:].startswith('"'):
                end = text.find('"', pos + 1)
                if end == -1:
                    raise SyntaxError("Unclosed string")
                value = text[pos + 1:end]
                self.tokens.append(Token(TokenType.STRING, value, self.line_num, pos))
                pos = end + 1
            elif text[pos:].startswith('->'):
                self.tokens.append(Token(TokenType.ARROW, '->', self.line_num, pos))
                pos += 2
            elif text[pos:].startswith('=>'):
                self.tokens.append(Token(TokenType.FAT_ARROW, '=>', self.line_num, pos))
                pos += 2
            elif text[pos:].startswith('..'):
                self.tokens.append(Token(TokenType.RANGE, '..', self.line_num, pos))
                pos += 2
            elif text[pos] == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line_num, pos))
                pos += 1
            elif text[pos] == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line_num, pos))
                pos += 1
            elif text[pos] == '*':
                self.tokens.append(Token(TokenType.STAR, '*', self.line_num, pos))
                pos += 1
            elif text[pos] == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', self.line_num, pos))
                pos += 1
            elif text[pos] == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line_num, pos))
                pos += 1
            elif text[pos] == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line_num, pos))
                pos += 1
            elif text[pos] == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line_num, pos))
                pos += 1
            elif text[pos] == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line_num, pos))
                pos += 1
            elif text[pos] == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line_num, pos))
                pos += 1
            elif text[pos] == '[':
                self.tokens.append(Token(TokenType.LBRACK, '[', self.line_num, pos))
                pos += 1
            elif text[pos] == ']':
                self.tokens.append(Token(TokenType.RBRACK, ']', self.line_num, pos))
                pos += 1
            elif text[pos] in ' \t':
                pos += 1  # skip extra space
            else:
                raise SyntaxError(f"Unexpected character: {text[pos]}")