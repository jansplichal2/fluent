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
        elif isinstance(expr, IfExpr):
            cond = self.eval_expr(expr.condition, env)
            if not isinstance(cond, bool):
                raise TypeError(f"If condition must be a boolean, got: {type(cond).__name__}")
            branch = expr.then_branch if cond else expr.else_branch
            if branch is None:
                return None
            local_env = Environment(parent=env)
            result = None
            for stmt in branch:
                result = self.eval_stmt(stmt, local_env)
            return result
        elif isinstance(expr, MatchExpr):
            value = self.eval_expr(expr.matched_expr, env)
            for case in expr.cases:
                if case.pattern == "_":
                    matched = True
                elif isinstance(case.pattern, int) or isinstance(case.pattern, str):
                    matched = value == case.pattern
                elif isinstance(case.pattern, str):
                    matched = env.get(case.pattern) == value
                else:
                    matched = False
                if matched:
                    return self.eval_expr(case.expr, env)
            raise ValueError(f"No match found for value: {value}")

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
