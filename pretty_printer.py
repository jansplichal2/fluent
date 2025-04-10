from fluent_ast import *
from parser import Parser

def pretty_print(node, indent=0):
    pad = "  " * indent

    if isinstance(node, list):
        for n in node:
            pretty_print(n, indent)
        return

    if isinstance(node, FnDecl):
        print(f"{pad}FnDecl(name={node.name})")
        for param in node.params:
            pretty_print(param, indent + 1)
        pretty_print(node.body, indent + 1)

    elif isinstance(node, FnParam):
        print(f"{pad}Param(name={node.name}, type={node.type_annotation})")

    elif isinstance(node, LetStmt):
        print(f"{pad}LetStmt(name={node.name})")
        pretty_print(node.value, indent + 1)

    elif isinstance(node, ExprStmt):
        print(f"{pad}ExprStmt")
        pretty_print(node.expr, indent + 1)

    elif isinstance(node, Number):
        print(f"{pad}Number(value={node.value})")

    elif isinstance(node, String):
        print(f"{pad}String(value={repr(node.value)})")

    elif isinstance(node, Var):
        print(f"{pad}Var(name={node.name})")

    elif isinstance(node, Binary):
        print(f"{pad}Binary(op={node.op})")
        pretty_print(node.left, indent + 1)
        pretty_print(node.right, indent + 1)

    elif isinstance(node, Call):
        print(f"{pad}Call(func={node.func})")
        for arg in node.args:
            pretty_print(arg, indent + 1)

    elif isinstance(node, IfExpr):
        print(f"{pad}IfExpr")
        print(f"{pad}  Condition:")
        pretty_print(node.condition, indent + 2)
        print(f"{pad}  Then:")
        pretty_print(node.then_branch, indent + 2)
        if node.else_branch:
            print(f"{pad}  Else:")
            pretty_print(node.else_branch, indent + 2)

    elif isinstance(node, MatchExpr):
        print(f"{pad}MatchExpr")
        print(f"{pad}  Matched:")
        pretty_print(node.matched_expr, indent + 2)
        print(f"{pad}  Cases:")
        for case in node.cases:
            pretty_print(case, indent + 2)

    elif isinstance(node, MatchCase):
        print(f"{pad}MatchCase(pattern={node.pattern})")
        pretty_print(node.expr, indent + 1)

    else:
        print(f"{pad}Unknown({node})")


if __name__ == '__main__':
    source = """
fn classify(x: Int)
  match x
    1 => "one"
    2 => "two"
    _ => if x > 2
      "many"
    else
      "other"
"""

    from pretty_printer import pretty_print
    ast = Parser(source).parse()
    pretty_print(ast)