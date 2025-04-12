from fluent_ast import (
    Number, String, Binary, Var, LetStmt, ExprStmt, FnDecl,
    Expr, Stmt, Call, IfExpr, MatchExpr, MatchCase, Return, Boolean
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


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class BuiltInFunction:
    def __init__(self, name, impl):
        self.name = name
        self.impl = impl

    def call(self, args):
        return self.impl(*args)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self._register_builtins()

    def eval_program(self, stmts: list[Stmt]):
        result = None
        for stmt in stmts:
            result = self.eval_stmt(stmt, self.global_env)
        return result

    def _register_builtins(self):
        self.global_env.set("print", BuiltInFunction("print", lambda *args: print(*args) or None))
        self.global_env.set("len", BuiltInFunction("len", self._len_builtin))

    def _len_builtin(self, value):
        if isinstance(value, (str, list)):
            return len(value)
        raise TypeError(f"len() expects a string or list, got {type(value).__name__}")

    def eval_stmt(self, stmt: Stmt, env: Environment):
        if isinstance(stmt, LetStmt):
            value = self.eval_expr(stmt.value, env)
            env.set(stmt.name, value)
            return value
        elif isinstance(stmt, FnDecl):
            env.set(stmt.name, stmt)
            return stmt
        elif isinstance(stmt, ExprStmt):
            return self.eval_expr(stmt.expr, env)
        elif isinstance(stmt, Return):
            value = self.eval_expr(stmt.expr, env)
            raise ReturnException(value)
        else:
            raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    def eval_expr(self, expr: Expr, env: Environment):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, String):
            return expr.value
        elif isinstance(expr, Var):
            return env.get(expr.name)
        elif isinstance(expr, Boolean):
            return expr.value
        elif isinstance(expr, Binary):
            if expr.op == "and":
                return self.eval_expr(expr.left, env) and self.eval_expr(expr.right, env)
            elif expr.op == "or":
                return self.eval_expr(expr.left, env) or self.eval_expr(expr.right, env)
            elif expr.op == "and not":
                return self.eval_expr(expr.left, env) and not self.eval_expr(expr.right, env)
            elif expr.op == "+":
                return self.eval_expr(expr.left, env) + self.eval_expr(expr.right, env)
            elif expr.op == "-":
                return self.eval_expr(expr.left, env) - self.eval_expr(expr.right, env)
            elif expr.op == "*":
                return self.eval_expr(expr.left, env) * self.eval_expr(expr.right, env)
            elif expr.op == "/":
                return self.eval_expr(expr.left, env) / self.eval_expr(expr.right, env)
            elif expr.op == ">":
                return self.eval_expr(expr.left, env) > self.eval_expr(expr.right, env)
            elif expr.op == "<":
                return self.eval_expr(expr.left, env) < self.eval_expr(expr.right, env)
            elif expr.op == ">=":
                return self.eval_expr(expr.left, env) >= self.eval_expr(expr.right, env)
            elif expr.op == "<=":
                return self.eval_expr(expr.left, env) <= self.eval_expr(expr.right, env)
            elif expr.op == "==":
                return self.eval_expr(expr.left, env) == self.eval_expr(expr.right, env)
            elif expr.op == "!=":
                return self.eval_expr(expr.left, env) != self.eval_expr(expr.right, env)
            else:
                raise NotImplementedError(f"Unsupported operator: {expr.op}")
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
        elif isinstance(expr, Call):
            fn = env.get(expr.func)
            args = [self.eval_expr(arg, env) for arg in expr.args]
            if isinstance(fn, FnDecl):
                local_env = Environment(parent=env)
                if len(expr.args) != len(fn.params):
                    raise ValueError(f"Function '{fn.name}' expects {len(fn.params)} arguments, got {len(expr.args)}")
                for param, arg in zip(fn.params, args):
                    local_env.set(param.name, arg)
                try:
                    result = None
                    for stmt in fn.body:
                        result = self.eval_stmt(stmt, local_env)
                    return result
                except ReturnException as re:
                    return re.value
            elif isinstance(fn, BuiltInFunction):
                return fn.call(args)
            else:
                raise TypeError(f"'{expr.func}' is not a function")
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
