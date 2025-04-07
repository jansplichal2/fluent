# 🗺️ Fluent Language Development Roadmap

This document outlines the staged development of the Fluent programming language. Each milestone builds upon the previous, with clear goals for language design, tooling, and ecosystem maturity.

---

## ✅ Phase 0: Foundation (Completed)
- [x] Tokenizer (lexer) with full position tracking
- [x] Unit tests for lexer including errors and edge cases
- [x] Draft grammar specification (v0.1)
- [x] Language design manifesto

---

## 🚧 Phase 1: Parser & AST
- [ ] Build recursive descent parser from token stream
- [ ] Define core AST node types and structure
- [ ] Handle function declarations, let bindings, expressions, if, match
- [ ] Include indentation-aware block parsing
- [ ] Implement tests for AST parsing and structure

---

## 🔧 Phase 2: Interpreter
- [ ] Basic expression evaluator (arithmetic, variables, function calls)
- [ ] Implement pattern matching evaluation
- [ ] Function environment and closures
- [ ] List and range evaluation
- [ ] Add REPL for testing expressions interactively

---

## 🧠 Phase 3: Type System
- [ ] Static type checker
- [ ] Type inference (simple Hindley–Milner core)
- [ ] Exhaustiveness checking in `match`
- [ ] Type annotations and error messages

---

## 🧱 Phase 4: Advanced Language Features
- [ ] Algebraic data types and variant constructors
- [ ] Traits and `impl` support
- [ ] Polymorphic function support (type variables)
- [ ] Function pipelines (`|>`)

---

## ⚙️ Phase 5: Tooling & Ecosystem
- [ ] Code formatter (`fluentfmt`)
- [ ] Linter and style checker
- [ ] Language server protocol (LSP) support
- [ ] Documentation generator
- [ ] Basic standard library: List, String, Map, Option, Result

---

## 🚀 Phase 6: Deployment Targets
- [ ] Compile to stack-based bytecode
- [ ] Implement VM or interpreter loop
- [ ] WebAssembly backend (WASM)
- [ ] CLI tools for running Fluent code (`fluent run file.fl`)

---

## 🌍 Phase 7: Open Source Release
- [ ] Public GitHub repo
- [ ] Contribution guide and code of conduct
- [ ] Language website with playground
- [ ] Package manager stub (`fluentpkg`)

---

## 📌 Ongoing Goals
- Simplicity and composability over features
- Clear, exhaustive error reporting
- Predictable and testable evaluation model
- Tooling that works out of the box

---

Fluent is a language that should feel like a tool you trust — readable, safe, and simple enough to carry in your head.
