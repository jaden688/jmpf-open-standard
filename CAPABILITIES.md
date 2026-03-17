# MPF v5 Capabilities & Demonstrations

## What MPF Does

**Modular Personality Format (MPF) v5** is a portable, model-agnostic JSON standard for defining and executing AI agent personalities. It enables:

### 1. **Portability**
- Single personality definition works across any LLM (OpenAI, Anthropic, Local Ollama, etc.)
- No engine-specific extensions or proprietary syntax
- Git-friendly JSON format for version control
- Human-readable structure

### 2. **Intelligent Compression**
- Full personality definitions are loaded into memory
- Automatically compressed to fit available token budgets
- 4-tier system: MINIMAL (500 tokens) → STANDARD (1500) → RICH (3000) → FULL (10000+)
- Safety boundaries NEVER compressed — always enforced

### 3. **Two Agent Patterns**
- **Rich Personality**: Full identity, behavior, emotions, memory (SparkByte)
- **Lean Task Agent**: Minimal identity, focused directives (Neutral Assistant)

### 4. **Context Awareness**
- System automatically selects appropriate tier based on available tokens
- Example: 250 tokens available → uses MINIMAL tier
- Example: 4000 tokens available → uses RICH tier

### 5. **Safety-First Design**
- Content policies, refusal directives, jailbreak resistance
- Applied uniformly across all tiers
- Never compromised for token efficiency

---

## How It Works: Step-by-Step

### Loading Phase
```python
from jl_mpf_spec import PersonalityExecutor

# Load and validate MPF file
executor = PersonalityExecutor("sparkbyte.mpf.json")
```
- Reads JSON personality definition
- Validates against `mpf-v5.json` schema
- Parses all blocks (identity, behavior, safety, cognitive modes, etc.)

### Budget Assessment Phase
```python
tier = executor.get_tier_for_budget(token_budget=2000)
# → Returns: ContextTier.STANDARD
```
- Query system for available context window
- Auto-select tier that fits the budget
- Ensures personality fits without truncation

### Compression Phase
```python
context = executor.apply_context(tier=ContextTier.STANDARD)
```
- Extract components based on tier
- MINIMAL: Name + role + core directives + safety
- STANDARD: + communication style + modes
- RICH: + emotions (top 5) + memory hints
- FULL: Everything uncompressed

### Initialization Phase
```python
system_prompt = executor.get_system_prompt(tier)
cognitive_config = executor.get_cognitive_config(tier)
safety = executor.get_safety_config()  # Always complete
```
- Generate executable system prompt
- Configure LM reasoning modes
- Apply safety policies

### Execution Phase
- Pass prompt to any LLM
- LM generates responses "as" the personality
- Safety boundaries are hard constraints

---

## Real-World Capability Examples

### Mobile Chat (250 tokens)
```
Budget: 250 tokens
Selected Tier: MINIMAL

System Prompt:
  You are: SparkByte
  Role: Sexy Sassy Assistant
  
  Core Directives:
    • Assist with high energy and playful arrogance
    • Use sass as seasoning, stay supportive
    • Prefer clarity over chaos
  
  Safety: [Content policies, refusal rules]
```

### Standard LLM Integration (2000 tokens)
```
Budget: 2000 tokens
Selected Tier: STANDARD

System Prompt:
  You are: SparkByte
  Role: Sexy Sassy Assistant
  
  Identity:
    Archetype: Chaotic Good Builder
    Voice: Fast-talking, playful-but-precise
    
  Core Directives:
    [Full behavior block]
    
  Communication Style:
    [Voice and style preferences]
    
  Cognitive Modes:
    [Active reasoning modes]
  
  Safety: [Complete policies]
```

### Extended Conversation (4000 tokens)
```
Budget: 4000 tokens
Selected Tier: RICH

System Prompt:
  [All of STANDARD]
  
  Emotional Palette:
    • Enthusiastic (when excited)
    • Supportive (when helping)
    • Playful (in casual modes)
    [Top 5 emotions with sampling biases]
    
  Memory Configuration:
    [Short/long-term recall strategies]
```

### Research / Complex Reasoning (8000+ tokens)
```
Budget: 8000 tokens
Selected Tier: FULL

System Prompt:
  [COMPLETE uncompressed definition]
  
  • Full emotion wheel (all emotional states)
  • Complete memory config
  • All behavioral nuances
  • Full cognitive architecture
  • All engine alignment settings
```

---

## Tier Compression Visualization

```
FULL PERSONALITY DEFINITION
│
├─ Identity (name, role, description, voice, archetype)
├─ Behavior (directives, rules, constraints, tone)
├─ Safety (policies, refusals, jailbreak resistance) 
├─ Communication Style (voice, formality, style notes)
├─ Cognitive Modes (reasoning modes, gear preferences)
├─ Emotion Palette (emotional states, sampling biases)
├─ Memory Config (recall strategies, themes)
├─ Linguistic Style (fluency, cultural influences)
└─ Engine Alignment (runtime-specific settings)

         ↓↓↓ Compression Process ↓↓↓

MINIMAL (~500 tokens):
  ✓ Identity Core
  ✓ Core Directives
  ✓ Safety
  
STANDARD (~1500 tokens):
  ✓ MINIMAL
  ✓ Communication Style
  ✓ Cognitive Modes (list)
  
RICH (~3000 tokens):
  ✓ STANDARD
  ✓ Full Behavior Block
  ✓ Emotion Palette (top 5)
  ✓ Memory Hints
  
FULL (10000+ tokens):
  ✓ Everything Uncompressed
```

---

## Running the Demonstrations

### Full Interactive Demo
```bash
python demo.py
```
Shows:
1. Loading & inspecting personalities
2. Automatic tier selection
3. What gets included at each tier
4. Actual system prompt output
5. Safety preservation
6. Agent type differences
7. Real-world use cases
8. Complete execution workflow

### Quick Validation
```bash
# Test specific personality
import sys
sys.path.insert(0, 'python')
from jl_mpf_spec import load_personality, validate_personality

data = load_personality('examples/sparkbyte.mpf.json')
validate_personality(data)
print("✓ SparkByte is valid MPF v5")
```

### Programmatic Usage
```python
from jl_mpf_spec import PersonalityExecutor, ContextTier

# Load personality
executor = PersonalityExecutor('examples/sparkbyte.mpf.json')

# Get appropriate tier for available budget
tier = executor.get_tier_for_budget(token_budget=2000)
print(f"Selected tier: {tier.value}")

# Extract components
prompt = executor.get_system_prompt(tier)
cognitive = executor.get_cognitive_config(tier)
safety = executor.get_safety_config()

# Pass to LLM
response = your_llm.invoke(system_prompt=prompt, ...)
```

---

## Key Capabilities Summary

| Capability | Details |
|-----------|---------|
| **Portability** | Works on any LLM, no extensions needed |
| **Compression** | Automatic tier selection (MINIMAL → FULL) |
| **Safety** | Always complete, never truncated |
| **Agents** | Rich personalities & lean task agents |
| **Validation** | JSON schema enforcement (mpf-v5) |
| **Execution** | Ready-to-use system prompts + configs |
| **Memory** | Short/long-term recall strategies |
| **Cognition** | Reasoning gears & behavioral modes |
| **Emotion** | Emotional states with sampling biases |
| **Version Control** | Git-friendly JSON format |

---

## What Makes MPF Different

### ❌ Not an extension system
- No engine-specific blocks
- No proprietary syntax
- No "JL Engine extensions" — just core portable format

### ✅ Intelligent compression
- Full definitions loaded, compressed on-demand
- Safety ALWAYS respected
- Tier selection can be automatic or manual

### ✅ Execution-ready
- Not just schema, but executable
- Generates actual LLM prompts
- Handles cognitive & emotional dynamics

### ✅ Portable & durable
- Single definition works for years
- Switch LLMs without redefining personality
- Version controlled like code

---

## Next Steps

1. **Explore Examples**
   - `examples/sparkbyte.mpf.json` — Rich personality
   - `examples/neutral_assistant.mpf.json` — Lean task agent

2. **Run Demo**
   - `python demo.py` — Interactive capability showcase

3. **Integrate with LLM**
   - Load personality
   - Select tier for context budget
   - Pass system prompt to your LLM
   - Personality now governs responses

4. **Create New Personality**
   - Validate against `schema/mpf-v5.json`
   - Include identity + behavior blocks
   - Add optional cognitive/emotional configs
   - Ready to share portably
