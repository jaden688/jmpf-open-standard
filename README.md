# JL MPF Spec (Modular Personality Format)

**A portable, model-agnostic JSON format for defining reusable AI personas.**

This project defines a simple, extensible personality schema that works across LLM tools.  
It separates an AI persona into clear parts:

- **Identity** – who the agent is
- **Behavior** – how it responds
- **Safety** – what boundaries it follows
- **Extensions** – optional engine-specific features (for example: `jl_engine`)

The goal is to make AI personas **shareable, consistent, and easy to integrate** across different systems, frameworks, and models.

---

## Why MPF?

Right now, every tool invents its own format for “personas”:

- character cards in chat UIs  
- hard-coded system prompts  
- YAML agent configs  
- app-specific presets

They’re not compatible, and they rarely support structured safety rules.

MPF provides:

✔️ A **standard JSON schema**  
✔️ A **tiny Python loader/validator**  
✔️ Example personalities  
✔️ Optional extensions that tools can safely ignore  

If a tool supports MPF, a persona file can be reused everywhere.

---

## Repository contents

```
schema/          JSON schema for MPF
examples/        Example .mpf.json personalities
python/          Reference Python loader + validator
README.md        This file
LICENSE          MIT license
```

---

## Core structure

An MPF file looks like this (simplified):

```json
{
  "schema_version": "mpf-jl-extensions-v1",
  "id": "sparkbyte-v1",
  "name": "SparkByte",
  "kind": "personality",

  "identity": { ... },
  "behavior": { ... },
  "safety":   { ... },

  "extensions": {
    "jl_engine": { ... }
  }
}
```

Tools that don’t understand a section (for example `extensions.jl_engine`) may **ignore it safely**.

---

## JSON schema

See:

```
schema/mpf-jl-extensions-v1.json
```

Use it to validate files in editors or CI pipelines.

---

## Python reference library

A tiny helper package is included:

```python
from jl_mpf_spec import load_personality, validate_personality

data = load_personality("examples/sparkbyte.mpf.json")
validate_personality(data)
```

This is intentionally lightweight.  
Other languages or tools can easily implement their own loaders.

---

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Validate a personality file

```bash
python -c "from jl_mpf_spec import load_personality, validate_personality; d = load_personality('examples/sparkbyte.mpf.json'); validate_personality(d); print('OK')"
```

If it prints **OK**, the file matches the schema.

---

## Who is this for?

- LLM app developers  
- agent framework authors  
- chatbot UI builders  
- anyone who wants reusable AI personas  

If you’ve ever copy-pasted the same system prompt into five tools,  
MPF exists to stop that pain.

---

## 🔧 Extensions

MPF supports engine-specific extensions without breaking compatibility.

This repository includes:

```
extensions.jl_engine
```

Other projects may define their own extension namespaces.  
Unknown extensions should simply be ignored by consumers.

---

## Roadmap

- [ ] Add CLI tool: `mpf validate file.mpf.json`
- [ ] Publish Python package to PyPI
- [ ] Add TypeScript reference loader
- [ ] Create library of community MPF personas
- [ ] Build import adapters for popular tools

---

## Contributing

We welcome:

- new example personalities  
- schema discussions and improvements  
- integrations and loaders  
- feedback from tool authors  

Open an Issue before large structural changes so we can align.

---

## MPF in plain English

**What MPF is:**  
A file that describes an AI personality in a clean format so different tools can use the same persona.

**Why extensions matter:**  
Tools can add extra fields under `extensions.*` without breaking compatibility.

**Why safety exists:**  
Safety isn’t about censorship — it’s about predictable boundaries and clearer expectations.

MPF doesn’t replace prompts or policies.  
It organizes them into a structure tools can agree on.

---

## Examples

Example MPF files live in:

```
examples/
```

They show:

- a neutral baseline assistant  
- a personality using JL extensions  

You can copy these and customize.

---

## Goals

- Make AI personalities portable  
- Encourage standardization instead of siloed formats  
- Provide a foundation other tools can build on  

PRs, issues, and discussion are welcome.

---

## License

MIT License.  
Use it, modify it, ship it — just credit the spec.

