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

---

## 🧭 Next Steps
- Parse function calls (e.g. `greet("Jan")`)
- Parse `match` expressions
- Parse `if` expressions
- Parse block-level control flow
- Start interpreting expressions

---
