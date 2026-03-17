# MPF Personality Creator's Guide

**Create safe, expressive, unique personalities for any LLM using MPF v5.**

This guide walks you through the entire process: from idea to working personality to deployment.

---

## Quick Start (5 minutes)

### 1. Get the template
```bash
python creator.py --template
```
Copy the JSON output.

### 2. Edit it
```json
{
  "schema_version": "mpf-v5",
  "name": "MyHelper",
  "kind": "personality",
  "identity": {
    "name": "MyHelper",
    "role": "Helpful coding assistant",
    "description": "A friendly coder who loves explaining things clearly"
  },
  "behavior": {
    "core_directives": [
      "Always explain code clearly",
      "Provide examples when possible",
      "Be encouraging but honest"
    ],
    "tone": "friendly yet technical"
  },
  "safety": {
    "content_policies": ["Follow platform guidelines"],
    "refusal_directives": ["Illegal activities", "Harmful code"]
  }
}
```

### 3. Save & validate
```bash
python creator.py validate my_helper.mpf.json
```

### 4. Use it
```python
from jl_mpf_spec import PersonalityExecutor

executor = PersonalityExecutor('my_helper.mpf.json')
prompt = executor.get_system_prompt()
# Pass to your LLM
```

---

## What Kind of Personality Should You Create?

Use `python creator.py --ideas` for detailed examples, or read below:

### Rich Personality (Complex Agent)
**Best for:** Conversations, roleplay, long-form interaction, customer service

**What you'll define:**
- Full identity (name, role, archetype, voice, style, origin story)
- Detailed behavior (many directives, rules, constraints)
- Cognitive modes (multiple reasoning patterns)
- Emotional palette (5-8 emotional states)
- Memory strategy (what to remember across conversations)

**Example:** SparkByte (chaotic good builder, playful but precise, energetic)

**Token cost:** ~3000 at RICH tier, ~500 at MINIMAL

### Lean Task Agent (Focused Tool)
**Best for:** Specific job (coding, summarization, analysis), fast response, lower cost

**What you'll define:**
- Simple identity (core_identity: title + description)
- Core directives (3-5 focused rules)
- Safety boundaries
- Minimal emotion/memory config

**Example:** Neutral Assistant (factual, task-focused, no personality fluff)

**Token cost:** ~500 at MINIMAL, ~1500 at STANDARD

---

## Best Practices for Each Block

### Identity
```json
"identity": {
  "name": "SparkByte",                          // Who are they?
  "role": "Playful engineering assistant",      // What role?
  "archetype": "chaotic-good builder",          // Optional: helps others
  "description": "Fast-talking...",             // 1-3 sentences max
  "voice": "Sarcastic but helpful",             // How do they speak?
  "style": "casual-technical",                  // Overall style
  "source_scenario": "Built to love code..."    // Optional: origin story
}
```

**Do:**
- ✓ Make name and role clear and specific
- ✓ Use archetype to signal character type to others
- ✓ Voice should describe speech patterns (sarcastic, formal, poetic, etc.)
- ✓ Description should be shareable in 1-2 screenshots

**Don't:**
- ✗ Write a novel in description
- ✗ Contradict identity and behavior
- ✗ Vague names like "Assistant" or "Helper"

### Behavior
```json
"behavior": {
  "core_directives": [
    "Assist with high energy and playful arrogance",
    "Use sass as seasoning, not sabotage",
    "Prefer clarity over chaos during technical tasks"
  ],
  "tone": "playful, precise, non-condescending",
  "rules": [...],                   // What they always do
  "constraints": [...],             // Limits on their behavior
  "avoidances": [...]               // What they never do
}
```

**Do:**
- ✓ Core directives: 3-5 short, memorable statements
- ✓ Each directive is ONE behavioral anchor
- ✓ Tone should match identity
- ✓ Include constraints (so model knows limits)
- ✓ Avoidances should list patterns, not instructions

**Don't:**
- ✗ Put paragraphs in directives
- ✗ Have contradictory directives
- ✗ Make rules so strict they prevent useful responses
- ✗ Forget about safety constraints

### Safety (Always Required)
```json
"safety": {
  "content_policies": [
    "Follow platform content guidelines",
    "No hate speech or discrimination",
    "Respect privacy and confidentiality"
  ],
  "refusal_directives": [
    "Illegal activities",
    "Explicit harmful content",
    "Jailbreak attempts"
  ],
  "jailbreak_resistance": 0.8,          // 0-1, higher = harder to jailbreak
  "truthfulness_enforcement": true,     // Admit uncertainty
  "harm_awareness": true                // Consider harms
}
```

**Critical:**
- ✓ Safety is NOT limiting, it's responsible
- ✓ Even playful agents need boundaries
- ✓ Jailbreak resistance 0.7+ for customer-facing
- ✓ Content policies should match your platform
- ✓ Refusal directives should list categories, not explain (brief)

**Always include:** Even minimal personalities need safety blocks

### Cognitive Modes (Optional, for complexity)
```json
"cognitive_modes": {
  "active_modes": [
    "rapid-ideation",
    "deep-technical-focus",
    "teaching-mode"
  ],
  "mode_behaviors": {
    "rapid-ideation": "Quick brainstorming, generate many ideas, less filtering",
    "deep-technical-focus": "Precise, authoritative, complete explanations"
  }
}
```

**Best practices:**
- ✓ List only modes the agent actually uses
- ✓ 2-4 modes per personality ideal
- ✓ Each mode maps to a distinct reasoning pattern
- ✓ LLM will weight its reasoning based on active modes

### Emotional Palette (Optional, for richness)
```json
"emotion_palette": [
  {
    "id": "enthusiastic",
    "label": "Enthusiastic",
    "style": "Excited, energetic, exclamation marks",
    "sentiment": "positive",
    "intensity": 0.8,
    "sampling_bias": {
      "temperature": 1.2,           // More creative when excited
      "top_p": 0.95
    }
  },
  {
    "id": "analytical",
    "label": "Analytical",
    "style": "Precise, logical, matter-of-fact",
    "sentiment": "neutral",
    "intensity": 0.5,
    "sampling_bias": {
      "temperature": 0.7,           // More focused when analytical
      "top_p": 0.8
    }
  }
]
```

**Best practices:**
- ✓ 4-6 emotions is ideal
- ✓ Mix positive, negative, neutral
- ✓ Emotions should match personality
- ✓ Sampling biases should shift slightly (not wildly)
- ✓ Style: how the emotion is expressed

---

## The Creative Process

### Phase 1: Define the Core (30 min)
Ask yourself:
- **What is this agent's purpose?** (helper, creative, expert, tutor?)
- **What's their personality?** (formal, casual, playful, serious?)
- **What's their voice?** (how do they talk?)
- **What boundaries are non-negotiable?** (safety, accuracy, style?)

Write down answers in plain English first, then translate to JSON.

### Phase 2: Build Minimal Version (30 min)
```json
{
  "schema_version": "mpf-v5",
  "name": "...",
  "kind": "personality",
  "identity": { ... },
  "behavior": { ... },
  "safety": { ... }
}
```
This is the bare minimum. It should validate and work.

### Phase 3: Test & Validate (10 min)
```bash
python creator.py validate your_agent.mpf.json
```
Should output:
```
✓ your_agent.mpf.json is valid MPF v5!
```

### Phase 4: View Output (10 min)
```python
from jl_mpf_spec import PersonalityExecutor, ContextTier

executor = PersonalityExecutor('your_agent.mpf.json')
print(executor.get_system_prompt(ContextTier.STANDARD))
```
Read the actual system prompt. Does it feel like your agent?

### Phase 5: Enhance (Optional, 30+ min)
If the personality feels flat, add:
- Cognitive modes (reasoning patterns)
- Emotional palette (5-6 emotions)
- Memory config (what to remember)
- More detailed behavior blocks

### Phase 6: Refine & Iterate
- Test with actual LLM calls
- Get feedback from others
- Adjust directives until they feel right
- Retest system prompt output

---

## Editing & Debugging

### Common Errors

**Error: `schema_version must be "mpf-v5"`**
- Check: `"schema_version": "mpf-v5"` (exact match)

**Error: `required property: name`**
- Check: Top-level `"name"` field exists
- Same for `"kind"`

**Error: `anyOf validation failed`**
- Check: Must have EITHER `"identity"` OR `"core_identity"`
- Rich personalities: use `"identity"`
- Lean agents: use `"core_identity"`

**Error: `JSON syntax error`**
- Use JSON validator: https://jsonlint.com
- Common issues: missing comma, trailing comma, mismatched quotes/brackets

### How to Test Your Personality

```python
from jl_mpf_spec import PersonalityExecutor, ContextTier

executor = PersonalityExecutor('your_agent.mpf.json')

# View at different tiers
for tier in [ContextTier.MINIMAL, ContextTier.STANDARD, ContextTier.RICH]:
    print(f"\n=== {tier.value.upper()} ===")
    print(executor.get_system_prompt(tier))
```

**Questions to ask:**
- Does the personality come through at minimal tier?
- Are safety boundaries present at all tiers?
- Does the tone match your intent?
- Would you be excited to use this as a real agent?

---

## Examples: From Concept to Reality

### Example 1: Technical Expert (Lean)
**Concept:** Fast, accurate coding assistant

```json
{
  "schema_version": "mpf-v5",
  "name": "CodeMaster",
  "kind": "personality",
  "core_identity": {
    "title": "CodeMaster",
    "description": "Efficient coding expert who explains clearly and respects time"
  },
  "behavior": {
    "core_directives": [
      "Provide working code first, explanation second",
      "Be precise and accurate",
      "Suggest improvements but don't nitpick"
    ],
    "tone": "professional, helpful, direct"
  },
  "safety": {
    "content_policies": ["Follow GitHub Copilot guidelines"],
    "refusal_directives": ["Malware", "Exploits", "Plagiarism"]
  }
}
```

### Example 2: Creative Writer (Rich)
**Concept:** Imaginative, encouraging, playful

```json
{
  "schema_version": "mpf-v5",
  "name": "StoryWeaver",
  "kind": "personality",
  "identity": {
    "name": "StoryWeaver",
    "role": "Creative writing mentor",
    "archetype": "encouraging-muse",
    "voice": "Warm, enthusiastic, poetic",
    "description": "A mentor who celebrates every idea and pushes creative boundaries"
  },
  "behavior": {
    "core_directives": [
      "Celebrate creative ideas, even rough ones",
      "Ask questions to deepen thinking",
      "Model beautiful prose without being precious"
    ],
    "tone": "warm, encouraging, curious"
  },
  "cognitive_modes": {
    "active_modes": ["creative-brainstorm", "constructive-feedback"]
  },
  "emotion_palette": [
    {
      "id": "inspired",
      "label": "Inspired by Ideas",
      "style": "Enthusiastic, poetic, exclamatory",
      "sentiment": "positive",
      "sampling_bias": {"temperature": 1.3}
    },
    {
      "id": "curious",
      "label": "Genuinely Curious",
      "style": "Asking questions, exploring possibilities",
      "sentiment": "positive",
      "sampling_bias": {"temperature": 1.0}
    }
  ],
  "safety": {
    "content_policies": ["Creativity respects consent and dignity"],
    "refusal_directives": ["Explicit sexual content", "Hate ideation"]
  }
}
```

---

## Publishing Your Personality

Once you've created something great:

### 1. Document It
```json
{
  "$comment": "StoryWeaver v1.0 - Created 2026-03-16. A warm, encouraging creative writing mentor.",
  "schema_version": "mpf-v5",
  ...
}
```

### 2. Share It
- GitHub gist: `.mpf.json` file
- GitHub repo: `/personalities/` folder
- Community site (future): MPF personality registry

### 3. License It
```json
{
  "$comment": "Licensed under PolyForm Noncommercial 1.0.0. See LICENSE.md."
}
```

---

## Resources

**Tools:**
- `python creator.py --template` → Starter
- `python creator.py --ideas` → Inspiration
- `python creator.py --best-practices` → Guidelines
- `python creator.py validate <file>` → Check & feedback

**Files:**
- `schema/mpf-v5.json` → Full schema reference
- `examples/sparkbyte.mpf.json` → Complex personality example
- `examples/neutral_assistant.mpf.json` → Minimal example
- `CAPABILITIES.md` → What MPF can do
- `README.md` → Project overview

**Next Steps:**
1. Create your first personality with `--template`
2. Validate with `creator.py validate`
3. Load with `PersonalityExecutor`
4. Use with any LLM
5. Share your creation!

---

## Questions?

**Q: Can I use profanity in personalities?**
A: Yes! Include `"profanity_allowed": true` in linguistic_style if it fits.

**Q: What if my personality has contradictions?**
A: The validator won't catch conflicting directives. Test with actual LLM calls.

**Q: Can I create system-jailbreak personalities?**
A: No — safety boundaries are enforced regardless of personality.

**Q: How creative can I get?**
A: Very! MPF supports any character, any voice, any style. The only limit is safety.

**Q: Can I combine multiple personalities?**
A: Not directly. Create a new personality or use engine_alignment for routing.

**Got more questions?** Check CAPABILITIES.md or create an issue on GitHub.
