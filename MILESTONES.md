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

### ✅ Parser
- Parses let bindings, literals, binary expressions, calls
- Parses function declarations, if/else, match expressions
- Supports precedence, nesting, and indentation blocks
- Unit tests cover edge cases and malformed syntax

### ✅ Interpreter (core)
- Environment model with parent scopes
- Evaluates:
  - let bindings and variable references
  - Binary, Var, Number, String
  - if expressions with strict boolean enforcement
  - match expressions with wildcard and if branches
- Pretty printer for visualizing AST structure

### ✅ Interpreter (functions)
- Evaluates user-defined functions:
  - Supports FnDecl, parameter binding, and local scoping
  - Evaluates arguments and executes body in isolated environment
  - Returns final expression value
- Handles error cases:
  - Calling undefined functions
  - Incorrect argument count
- Full test coverage for function evaluation

---

## 🧭 Next Steps
- Add built-in functions (e.g. `print`, `length`)
- Support explicit return values from functions
- Add Boolean literals and logic operators (`and`, `or`, `not`)
- Implement type annotations and basic type checking
- Build REPL and CLI runner
- Begin packaging and LSP/editor support

---
