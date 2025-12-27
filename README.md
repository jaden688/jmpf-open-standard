# JL MPF Personality Spec (with JL Extensions)

This repository defines an open, model‑agnostic personality format.

The core is intentionally simple and reusable (`identity`, `behavior`, `safety`).
Advanced features for the JL Engine live under the namespaced block:

```
"extensions": { "jl_engine": { ... } }
```

Tools that don't understand the extension can safely ignore it.

## Contents
- JSON Schema for validation
- Example personalities
- A tiny Python reference loader/validator
