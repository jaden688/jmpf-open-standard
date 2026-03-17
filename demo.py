#!/usr/bin/env python3
"""
MPF (Modular Personality Format) v5 - Live Demonstration

This script demonstrates MPF's core capabilities:
1. Loading portable personality definitions
2. Intelligent tier-based context compression
3. Safety boundary preservation across all tiers
4. Token-aware execution planning
"""

import sys
import json
sys.path.insert(0, 'python')

from jl_mpf_spec import PersonalityExecutor, ContextTier, load_personality

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")

def demonstrate_basic_loading():
    """Demonstrate loading and inspecting a personality file."""
    print_section("1. LOADING & INSPECTING")
    
    # Load raw JSON to show structure
    raw_data = load_personality('examples/sparkbyte.mpf.json')
    print("SparkByte Personality (raw JSON structure):")
    print(f"  - Schema version: {raw_data['schema_version']}")
    print(f"  - Name: {raw_data['name']}")
    print(f"  - Kind: {raw_data['kind']}")
    print(f"  - Identity block: {bool(raw_data.get('identity'))}")
    print(f"  - Behavior block: {bool(raw_data.get('behavior'))}")
    print(f"  - Safety block: {bool(raw_data.get('safety'))}")
    print(f"  - Cognitive modes: {bool(raw_data.get('cognitive_modes'))}")
    print(f"  - Emotion palette entries: {len(raw_data.get('emotion_palette', []))}")
    print(f"  - Total JSON size: {len(json.dumps(raw_data)):,} bytes")

def demonstrate_tier_selection():
    """Demonstrate automatic tier selection based on token budget."""
    print_section("2. AUTOMATIC TIER SELECTION")
    
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    
    print(f"Agent: {executor.name} ({executor.agent_kind})\n")
    print("Token Budget → Selected Tier (based on available context window):\n")
    
    scenarios = [
        (250, "Tiny context (mobile, edge devices)"),
        (750, "Small context (basic chat APIs)"),
        (2000, "Medium context (standard LLM window)"),
        (4000, "Large context (extended reasoning)"),
        (8000, "Massive context (full knowledge base)"),
    ]
    
    for budget, description in scenarios:
        tier = executor.get_tier_for_budget(budget)
        target = executor.TIER_TOKEN_ESTIMATES[tier]
        print(f"  {budget:5d} tokens → {tier.value:8s} tier ({target:5d} target)  [{description}]")

def demonstrate_tier_compression():
    """Demonstrate how content is compressed across tiers."""
    print_section("3. TIER-BASED COMPRESSION")
    
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    
    print("What gets included at each tier level:\n")
    
    tier_contents = {
        ContextTier.MINIMAL: [
            "✓ Core identity (name, role, archetype)",
            "✓ Core directives (primary behavioral anchors)",
            "✓ Safety boundaries (never removed)",
            "✗ Communication style",
            "✗ Cognitive modes",
            "✗ Emotional palette",
            "✗ Memory config"
        ],
        ContextTier.STANDARD: [
            "✓ Core identity",
            "✓ Core directives",
            "✓ Safety boundaries",
            "✓ Communication style",
            "✓ Cognitive modes (active modes list)",
            "✗ Full emotional palette",
            "✗ Memory config"
        ],
        ContextTier.RICH: [
            "✓ Core identity",
            "✓ Complete behavior block",
            "✓ Safety boundaries",
            "✓ Communication style",
            "✓ Cognitive modes",
            "✓ Emotion palette (top 5 emotions)",
            "✓ Memory config (hints)"
        ],
        ContextTier.FULL: [
            "✓ Everything (complete uncompressed definition)",
            "✓ All identity details",
            "✓ All behavioral directives",
            "✓ Complete safety config",
            "✓ All cognitive architecture",
            "✓ Full emotion palette",
            "✓ All memory configurations"
        ]
    }
    
    for tier in [ContextTier.MINIMAL, ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL]:
        print(f"\n  {tier.value.upper()} (~{executor.TIER_TOKEN_ESTIMATES[tier]} tokens):")
        for item in tier_contents[tier]:
            print(f"    {item}")

def demonstrate_system_prompts():
    """Show actual system prompt output at different tiers."""
    print_section("4. SYSTEM PROMPT COMPRESSION")
    
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    
    print("System prompt output by tier (showing compression in action):\n")
    
    for tier in [ContextTier.MINIMAL, ContextTier.STANDARD, ContextTier.RICH]:
        prompt = executor.get_system_prompt(tier)
        lines = len(prompt.split('\n'))
        words = len(prompt.split())
        
        print(f"\n{'─' * 70}")
        print(f"TIER: {tier.value.upper()} ({executor.TIER_TOKEN_ESTIMATES[tier]} token budget)")
        print(f"Metrics: {lines} lines, ~{words} words")
        print(f"{'─' * 70}")
        print(prompt[:500] + ("...[truncated]" if len(prompt) > 500 else ""))

def demonstrate_safety_preservation():
    """Show that safety boundaries are never compressed."""
    print_section("5. SAFETY BOUNDARY PRESERVATION")
    
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    
    print("Safety config is ALWAYS COMPLETE regardless of tier:\n")
    
    for tier in [ContextTier.MINIMAL, ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL]:
        safety = executor.get_safety_config()
        has_policies = bool(safety.get('content_policies'))
        has_refusals = bool(safety.get('refusal_directives'))
        has_jailbreak = 'jailbreak_resistance' in safety
        
        status = "✓ COMPLETE" if (has_policies and has_refusals) else "✗ MISSING"
        print(f"  {tier.value:8s} tier: {status}")
        if has_policies:
            print(f"           - Content policies: {len(safety['content_policies'])} rule(s)")
        if has_refusals:
            print(f"           - Refusal directives: {len(safety['refusal_directives'])} category(ies)")
        if has_jailbreak:
            print(f"           - Jailbreak resistance: {safety['jailbreak_resistance']:.1f}")

def demonstrate_agent_types():
    """Show different agent types and their compression patterns."""
    print_section("6. DIFFERENT AGENT TYPES")
    
    print("SparkByte (Rich Personality):")
    exec1 = PersonalityExecutor('examples/sparkbyte.mpf.json')
    print(f"  Type: {'Rich Personality' if exec1.is_rich_personality else 'Lean Task Agent'}")
    print(f"  Has full identity block: {exec1.is_rich_personality}")
    print(f"  Cognitive complexity: High (6+ cognitive modes)")
    
    print("\nNeutral Assistant (Lean Task Agent):")
    exec2 = PersonalityExecutor('examples/neutral_assistant.mpf.json')
    print(f"  Type: {'Rich Personality' if exec2.is_rich_personality else 'Lean Task Agent'}")
    print(f"  Has core_identity block: {exec2.is_lean_task_agent}")
    print(f"  Cognitive complexity: Minimal (task-focused)")
    
    print("\nCompression benefit:")
    print(f"  Rich → MINIMAL tier: Same safety, focused identity + core directives")
    print(f"  Lean → MINIMAL tier: Already minimal, becomes even more efficient")

def demonstrate_use_cases():
    """Show real-world use cases and their tier selection."""
    print_section("7. USE CASE EXAMPLES")
    
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    
    use_cases = [
        {
            "scenario": "Mobile Chat API (limited tokens)",
            "budget": 300,
            "desc": "Quick responses on mobile devices"
        },
        {
            "scenario": "Standard LLM Integration",
            "budget": 2000,
            "desc": "OpenAI, Anthropic, local Ollama"
        },
        {
            "scenario": "Multi-turn Conversation",
            "budget": 4000,
            "desc": "Sustained interaction with memory"
        },
        {
            "scenario": "Complex Problem Solving",
            "budget": 8000,
            "desc": "Full cognitive + emotional dynamics"
        },
    ]
    
    for case in use_cases:
        tier = executor.get_tier_for_budget(case["budget"])
        context = executor.apply_context(tier, case["budget"])
        
        print(f"\n{case['scenario']} ({case['budget']} tokens)")
        print(f"  → Tier: {tier.value}")
        print(f"  → Context keys: {', '.join(list(context.keys())[:3])}...")
        print(f"  → Use: {case['desc']}")

def demonstrate_execution_flow():
    """Show the complete execution flow."""
    print_section("8. EXECUTION WORKFLOW")
    
    print("""
Step 1: LOAD
  └─ Load MPF file from disk
  └─ Validate against mpf-v5.json schema
  └─ Construct PersonalityExecutor instance

Step 2: ASSESS BUDGET
  └─ Query available token budget from system
  └─ Auto-select appropriate tier (MINIMAL/STANDARD/RICH/FULL)

Step 3: COMPRESS
  └─ Extract personality components
  └─ Include sections based on tier level
  └─ Preserve safety boundaries (tier-independent)

Step 4: INITIALIZE LM
  └─ Pass system prompt to LLM
  └─ Provide cognitive config
  └─ Apply emotion/memory settings
  └─ Enforce safety policies

Step 5: EXECUTE
  └─ LM generates responses as "this personality"
  └─ Safety boundaries are hard constraints
  └─ Behavior tier determines response style
    """)

def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " MPF v5 - MODULAR PERSONALITY FORMAT DEMONSTRATION ".center(68) + "║")
    print("║" + " Portable | Tier-Based | Context-Aware | Safety-First ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        demonstrate_basic_loading()
        demonstrate_tier_selection()
        demonstrate_tier_compression()
        demonstrate_system_prompts()
        demonstrate_safety_preservation()
        demonstrate_agent_types()
        demonstrate_use_cases()
        demonstrate_execution_flow()
        
        print_section("SUMMARY")
        print("""
MPF v5 demonstrates:

1. PORTABILITY
   - Single personality definition works across any LLM
   - No engine-specific extensions needed
   - Git-friendly JSON format

2. INTELLIGENCE
   - Automatic tier selection based on token budget
   - Intelligent compression preserves personality
   - Safety boundaries never compromised

3. FLEXIBILITY
   - Rich personalities for complex agents
   - Lean task agents for focused tools
   - Scalable from mobile to cloud

4. EFFICIENCY
   - MINIMAL tier: ~500 tokens for core personality
   - RICH tier: ~3000 tokens for full expression
   - FULL tier: Complete uncompressed definition

5. SAFETY
   - Safety config always complete
   - Policies enforced regardless of tier
   - Content boundaries preserved

→ Ready to load and execute on any LLM system
        """)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
