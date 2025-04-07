# 🪧 Fluent Language Design Manifesto

## 🌱 Philosophy

**Fluent is a language for humans who think.**  
It is designed to be expressive, predictable, and structurally honest — a tool that amplifies reasoning, not complexity.

Fluent is not about novelty — it’s about clarity.  
It borrows the best from proven paradigms and reshapes them into a coherent whole.

> *"Write code that reads like thought. Build systems that fit in your head."*

---

## 🔷 Core Design Principles

### 1. 🧠 **Model reality with types**

The type system is not a constraint — it's a **modeling tool**.  
Algebraic data types, traits, and exhaustive matching make it easy to represent real-world concepts without hacks.

If something can be incorrect, you should be able to prevent it with a type.  
If something *must* be handled, the compiler will remind you.

---

### 2. 🔎 **Everything is an expression**

There are no statements — only expressions that evaluate to values.  
This makes control flow composable, functions consistent, and code more algebraic.

```fluent
let result = if x > 0
  "positive"
else
  "negative"
```

---

### 3. 🪶 **Simplicity by default, power when needed**

Fluent is designed to be **usable on day one** without boilerplate.  
But it doesn’t limit expressiveness — it just avoids unnecessary ceremony.

You don't need to subclass, override, or annotate — you just define **shapes and behavior**.

---

### 4. 🛡️ **Safety without friction**

- No nulls
- No implicit fallthroughs
- No hidden control flow
- No runtime exceptions from forgetting a case

You write what you mean. The type system and runtime **enforce the contract**.

---

### 5. 📐 **Predictable semantics, regular grammar**

Every construct has a **clear meaning**, and every construct can appear in **any expression context**.

Indentation defines structure (like Python), and **synthetic tokens** like `INDENT` and `DEDENT` make parsing regular.

This makes Fluent **easy to read**, **easy to parse**, and **easy to tool**.

---

### 6. 🧩 **Composability over hierarchy**

There is no class inheritance.  
Behavior is modeled with **traits**, and data with **variants**.

This encourages:
- Explicit modeling over accidental structure
- Flat composition over deep hierarchy
- Capabilities over taxonomies

---

## 💡 What Fluent Leaves Behind

| Feature                    | Why It’s Out                  |
|----------------------------|-------------------------------|
| Class inheritance          | Too rigid and fragile         |
| Statements (if, return...) | Break composability           |
| Null / undefined           | Leads to runtime ambiguity    |
| Exceptions for control flow| Makes logic invisible         |
| Heavy DSLs/macros          | Hides true program shape      |

---

## 🧭 Vision

Fluent should scale:

- From scripts to systems
- From learning to production
- From individual devs to teams

…but always with a core promise: **you can understand what the code does by reading it**.

---

## 🛠️ Future Directions (Always Tentative)

- Traits with generics and associated types
- First-class async and concurrency
- Type inference with Hindley–Milner-style constraints
- Lightweight effect system for I/O purity tracking
- WASM compilation target
- Integrated formatting, linting, and REPL tooling
