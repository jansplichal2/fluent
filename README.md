# Fluent Language Grammar v0.1

## 🧹 Program Structure

```
program         ::= { statement NEWLINE } EOF
statement       ::= fn_decl
                  | let_stmt
                  | expr_stmt
```

---

## 🧱 Function Declarations

```
fn_decl         ::= "fn" IDENT "(" [ param_list ] ")" [ "->" type ] block

param_list      ::= param { "," param }
param           ::= IDENT ":" type
```

---

## 🔢 Let Bindings

```
let_stmt        ::= "let" IDENT [ ":" type ] "=" expr
```

---

## ➟ Blocks and Indentation

```
block           ::= NEWLINE INDENT { statement NEWLINE } DEDENT
```

---

## 🧠 Expressions

```
expr            ::= literal
                  | IDENT
                  | call_expr
                  | binary_expr
                  | if_expr
                  | match_expr

call_expr       ::= IDENT "(" [ expr_list ] ")"
expr_list       ::= expr { "," expr }

binary_expr     ::= expr bin_op expr
bin_op          ::= "+" | "-" | "*" | "/"
```

---

## 🔍 Match Expression

```
match_expr      ::= "match" expr block
match_case      ::= pattern "=>" expr
pattern         ::= NUMBER | IDENT | "_"
```

---

## 🔀 If Expression

```
if_expr         ::= "if" expr block [ "else" block ]
```

---

## 🔣 Literals

```
literal         ::= NUMBER
                  | STRING
                  | list_literal

list_literal    ::= "[" expr ".." expr "]"
```

---

## 🄤 Types

```
type            ::= "Int" | "String" | "Bool" | IDENT  ; user-defined types later
```

---

## 🦾 Tokens (Terminal symbols)

```
IDENT           ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER          ::= [0-9]+
STRING          ::= '"' { any_char_except_quote_or_backslash } '"'

INDENT          ::= inferred via leading spaces
DEDENT          ::= inferred via reduction in leading spaces
NEWLINE         ::= '\n' or '\r\n'
EOF             ::= end of input
```

---

## ✨ Planned but Not Yet Implemented

This grammar allows for future additions like:

- `type` declarations (ADTs / enums / structs)
- pipelines or method chains: `list.map(f).filter(g)`
- anonymous functions: `fn(x) => x + 1`
- basic error handling: `try`, `result`, etc.
- async blocks or `spawn`

---

## 📌 Notes

- The grammar is indentation-sensitive (like Python), so INDENT/DEDENT are **synthetic tokens**, not characters.
- All control structures are **expressions**, not statements.
- There’s no return keyword in function bodies yet — they just return the last expression (like in Elixir or Scala).

