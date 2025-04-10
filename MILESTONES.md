# ✅ Fluent Language - Development Milestones

This document tracks completed work as we build the Fluent programming language step by step.

---

## 📅 Milestones Completed (as of now)

### ✅ Lexer
- Token types defined (keywords, literals, symbols)
- Position tracking for line and column
- Indentation-aware (INDENT/DEDENT/NEWLINE)
- Unit tests for valid tokens and error cases

### ✅ Grammar Spec
- Written in EBNF-style reference (`Fluent Grammar v0.1`)
- Covers expressions, function declarations, types, and match

### ✅ Design Manifesto
- Fluent Language Manifesto drafted
- Outlines philosophy: simplicity, types-as-models, expression-oriented

### ✅ Roadmap
- Phases 0–7 defined (Lexer → LSP → Deployment)
- Daily progress follows this roadmap

### ✅ AST Layer
- Core AST nodes defined in `fluent_ast.py`
- Covers: LetStmt, FnDecl, ExprStmt, Binary, Var, Number, String, MatchExpr, etc.

### ✅ Parser (partial)
- Parses `let` bindings
- Parses integer and string literals
- Handles variable references
- Parses binary expressions with precedence (`+`, `*`, etc.)
- Supports parentheses for grouping
- Supports expression statements
- Parses function declarations with:
  - Positional typed parameters
  - Optional return type
  - Indented body as block
- Unit tests added for all of the above

### ✅ Parser (continued)
- Parses function calls: `foo(1 + 2)`
- Handles call chaining and nested expressions
- Parses `if` expressions with optional `else` branches
- Supports nested `if` (as `else if`) using recursion
- Parses `match` expressions with:
  - Literal patterns (`1`, `"x"`)
  - Variable patterns (`x`)
  - Wildcard patterns (`_`)
- Unit tests added for all of the above
- Comparison operators added and integrated: `>`, `<`, `==`, `!=`, etc.

### ✅ Interpreter (initial)
- Environment model with parent scopes
- Evaluates:
  - `let` bindings and variable references
  - `ExprStmt`, `Binary`, `Var`, `Number`, `String`
  - Function calls (stub-ready)
  - `if` expressions with strict boolean enforcement
  - `match` expressions with:
    - Literal patterns
    - Wildcard (`_`) patterns
    - Embedded expressions (e.g. `if` in match arms)
- Pretty printer for visualizing AST structure
- Full test coverage for all interpreter functionality

---

## 🧭 Next Steps
- Implement user-defined function evaluation
- Add built-in functions (e.g. print, length)
- Expand type annotations (Bool, custom types)
- Implement type checking phase
- Build REPL and CLI tooling
- Start packaging and LSP integration

---