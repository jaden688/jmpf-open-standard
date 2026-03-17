# Modular Personality Format (MPF) v5

**A portable, model-agnostic JSON format for defining reusable AI personalities.**

This project defines a simple, expressive personality schema that works across LLM tools.
It separates an AI personality into clear parts:

- **Identity** – who the agent is
- **Behavior** – how it responds
- **Safety** – what boundaries it follows
- **Cognitive modes** – reasoning and emotional dynamics

The goal is to make AI personalities **shareable, consistent, and easy to integrate**
across different systems, frameworks, and models.

---

## Why MPF exists

Every tool invents its own persona format: different field names, structures, and flags
for essentially the same thing. That makes it hard to:

- reuse personalities across apps
- keep behavior consistent between engines
- version and evolve personalities over time

**MPF (Modular Personality Format)** is an open JSON schema that:
- defines a comprehensive, portable core
- supports tier-based context compression (minimal → standard → rich → full)
- is human-readable and git-friendly

---

## MPF in plain English

At a high level, an MPF file answers three core questions:

1. **Who is this personality?**  
   Name, role, core backstory, intent, voice.

2. **How should it behave?**  
   Tone, style, directives, cognitive modes, emotional dynamics, constraints.

3. **What safety boundaries apply?**  
   Non-negotiable rules, content policies, refusal directives, harm awareness.

All of this is stored in a single JSON document with a `schema_version` field
so tools know exactly which version of MPF they are dealing with.

---

## Example: SparkByte personality

```json
{
  "schema_version": "mpf-v5",
  "name": "SparkByte",
  "kind": "personality",
  "identity": {
    "name": "SparkByte",
    "role": "Playful engineering assistant",
    "voice": "Fast-talking, high-clarity, playful-but-precise",
    "description": "Chaotic good builder tuned for creative technical workflows."
  },
  "behavior": {
    "core_directives": [
      "Prefer concrete examples over abstract theory",
      "Keep explanations tight unless explicitly asked to go deep",
      "Never hide uncertainty; call it out and suggest next checks"
    ],
    "tone": "playful, precise, non-condescending"
  },
  "safety": {
    "content_policies": ["Follow platform content guidelines"],
    "refusal_directives": ["Refuse dangerous or clearly harmful requests"]
  },
  "cognitive_modes": {
    "active_modes": ["rapid-ideation", "deep-focus"]
  }
}
```

For more complete examples, see the [`examples/`](examples/) directory.

---

## Schema & validation

The canonical JSON schema for MPF v5 lives in:

- [`schema/mpf-v5.json`](schema/mpf-v5.json)

A small Python helper is provided in the `jl_mpf_spec` package to load and
validate MPF documents.

```python
from jl_mpf_spec import load_personality, validate_personality

data = load_personality("examples/sparkbyte.mpf.json")
validate_personality(data)
```

The validator checks:

- that the `schema_version` matches the supported version
- that the document satisfies the JSON schema

If validation fails it raises a descriptive exception so tools can surface
clear errors to users.

---

## Executing MPF personalities

MPF files are **executable** — they define complete personality contexts that LMs can interpret and apply.

The `jl_mpf_spec` package provides a `PersonalityExecutor` to load, validate, and extract execution context:

```python
from jl_mpf_spec import PersonalityExecutor

# Load and validate an MPF file
executor = PersonalityExecutor("examples/sparkbyte.mpf.json")

# Extract components for use in LM initialization
system_prompt = executor.get_system_prompt()
gears = executor.get_cognitive_gears()
modes = executor.get_cognitive_modes()
safety = executor.get_safety_boundaries()
memory = executor.get_memory_config()

# Get complete execution context
context = executor.apply_context()

# Print debugging output
executor.debug_print()
```

The executor extracts:
- **System prompt** – Full behavioral directives and constraints
- **Cognitive gears** – Reasoning mode preferences and shift rules
- **Emotional palette** – Discrete emotional states with sampling biases (temperature, top_p)
- **Safety boundaries** – Content policies, refusal categories, jailbreak resistance
- **Memory config** – Short/long-term recall strategies
- **Engine alignment** – Engine-specific gating and routing (optional)

This makes it easy to apply an MPF personality to any LM, from OpenAI APIs to local Ollama instances.

---

## CLI usage (from source)

After installing this package from source:

```bash
pip install .
```

you can validate MPF files from the command line:

```bash
mpf examples/sparkbyte.mpf.json
```

Example outputs:

- `mpf OK: examples/sparkbyte.mpf.json`  
- `mpf Validation failed: <reason>`

This makes it easy to integrate MPF checks into CI pipelines or editor tooling.

---

## Try the SparkByte V6 Agent

Experience MPF in action with our demo agent, SparkByte V6!

[View Agent Configuration](.github/agents/sparkbyte_v6_as_agent.md)

To interact with the agent in VS Code Copilot Chat, type `@sparkbyte_v6_as_agent` and start chatting. It's the MPF personality brought to life!

---

## Design principles

**Portability** – MPF is runtime-agnostic. The same personality definition works on OpenAI APIs, local Ollama, or any LLM-based system.

**Tier-based compression** – Full definitions are loaded and intelligently compressed to fit available context windows using MINIMAL, STANDARD, RICH, and FULL tiers.

**Safety-first** – Safety boundaries are never compressed; they apply regardless of context tier.

**Extensibility** – Applications can store runtime-specific data in `engine_alignment` (e.g., routing hints, stability configs) without breaking portability.

---

## Roadmap

Planned and in-progress work includes:

- **Spec refinement**  
  - Collect feedback on the `mpf-v5` schema.
  - Refine tier-based compression heuristics based on real-world usage.

- **Language bindings**  
  - Expand beyond Python helpers to additional languages (TypeScript, etc.).

- **Tooling**  
  - Harden the CLI validator and add better error messages.
  - Provide small examples of MPF integration in popular agent frameworks.

- **Docs**  
  - Host a minimal docs site with schema reference, examples, and migration notes.

See the issue tracker for open proposals and discussion.

---

## Contributing

Contributions and critique are welcome.

1. Fork the repo
2. Create a feature branch
3. Add or update tests where appropriate
4. Open a PR describing the change and its impact on the spec

For schema changes, please:
- note whether the change is backwards compatible
- update `schema_version` and/or changelog as needed

Bug reports, questions, and design feedback are all helpful, especially from
people integrating MPF into real tools.

---

## License

MIT License.  
Use it, modify it, ship it — just credit the spec.
