from fluent_ast import (
    Number, String, Binary, Var, LetStmt, ExprStmt, FnDecl,
    Expr, Stmt, Call, IfExpr, MatchExpr, MatchCase
)


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.values[name] = value


class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def eval_program(self, stmts: list[Stmt]):
        result = None
        for stmt in stmts:
            result = self.eval_stmt(stmt, self.global_env)
        return result

    def eval_stmt(self, stmt: Stmt, env: Environment):
        if isinstance(stmt, LetStmt):
            value = self.eval_expr(stmt.value, env)
            env.set(stmt.name, value)
            return value
        elif isinstance(stmt, ExprStmt):
            return self.eval_expr(stmt.expr, env)
        else:
            raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    def eval_expr(self, expr: Expr, env: Environment):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, String):
            return expr.value
        elif isinstance(expr, Var):
            return env.get(expr.name)
        elif isinstance(expr, Binary):
            left = self.eval_expr(expr.left, env)
            right = self.eval_expr(expr.right, env)
            return self.apply_op(expr.op, left, right)
        else:
            raise NotImplementedError(f"Unsupported expression: {type(expr)}")

    def apply_op(self, op: str, left, right):
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        else:
            raise ValueError(f"Unknown operator: {op}")
