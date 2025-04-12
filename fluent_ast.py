from dataclasses import dataclass
from typing import List, Optional, Union

# === Expressions ===


@dataclass
class Expr:
    pass


@dataclass
class Number(Expr):
    value: int


@dataclass
class String(Expr):
    value: str


@dataclass
class Var(Expr):
    name: str


@dataclass
class Binary(Expr):
    left: Expr
    op: str
    right: Expr


@dataclass
class Call(Expr):
    func: str
    args: List[Expr]


@dataclass
class IfExpr(Expr):
    condition: Expr
    then_branch: List['Stmt']
    else_branch: Optional[List['Stmt']]


@dataclass
class MatchCase:
    pattern: Union[int, str, "_"]
    expr: Expr


@dataclass
class MatchExpr(Expr):
    matched_expr: Expr
    cases: List[MatchCase]


@dataclass
class ListLiteral(Expr):
    start: Expr
    end: Expr

# === Statements ===


@dataclass
class Stmt:
    pass


@dataclass
class LetStmt(Stmt):
    name: str
    type_annotation: Optional[str]
    value: Expr


@dataclass
class FnParam:
    name: str
    type_annotation: str


@dataclass
class FnDecl(Stmt):
    name: str
    params: List[FnParam]
    return_type: Optional[str]
    body: List[Stmt]


@dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclass
class Return(Stmt):
    expr: Expr


@dataclass
class Boolean(Expr):
    value: bool


@dataclass
class ListLiteral(Expr):
    elements: list