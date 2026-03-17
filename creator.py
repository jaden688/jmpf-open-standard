#!/usr/bin/env python3
"""
MPF Personality Creator & Guide

Interactive tool to help users create new personalities with guidance,
validation feedback, and best practice suggestions.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, 'python')

from jl_mpf_spec import PersonalityExecutor, load_personality, validate_personality


def print_header(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def show_starter_template():
    """Show a minimal starter template."""
    print_header("STARTER TEMPLATE - Minimal Personality")
    template = {
        "schema_version": "mpf-v5",
        "name": "Your Agent Name",
        "kind": "personality",
        "identity": {
            "name": "Your Agent Name",
            "role": "What role does this agent play?",
            "archetype": "Optional: Character archetype (e.g., 'helper', 'instructor')",
            "description": "Who is this agent? What's their personality?"
        },
        "behavior": {
            "core_directives": [
                "Primary behavioral anchor 1",
                "Primary behavioral anchor 2",
                "Primary behavioral anchor 3"
            ],
            "tone": "What tone should they use? (e.g., 'helpful', 'playful', 'formal')"
        },
        "safety": {
            "content_policies": [
                "Content policy 1 (e.g., 'Follow platform guidelines')"
            ],
            "refusal_directives": [
                "Category 1 - what kinds of requests to refuse"
            ]
        }
    }
    print(json.dumps(template, indent=2))
    print("\n→ Copy this, edit it, save as your_personality.mpf.json")


def show_personality_ideas():
    """Show examples of different personality types."""
    print_header("PERSONALITY IDEAS - What to Create")
    examples = {
        "Rich Personality": {
            "Use case": "Complex agent with multiple modes, emotions, deep character",
            "Includes": [
                "Full identity (archetype, voice, style, source story)",
                "Detailed behavior (directives, rules, constraints)",
                "Cognitive modes (reasoning patterns, gear preferences)",
                "Emotional palette (5+ emotional states with sampling biases)",
                "Memory configuration (recall strategies)"
            ],
            "Why": "For conversations that need personality depth and consistency"
        },
        "Lean Task Agent": {
            "Use case": "Focused tool for specific job (coding, writing, analysis)",
            "Includes": [
                "core_identity (title + description only)",
                "Core directives (3-5 focused behavioral rules)",
                "Safety boundaries",
                "Minimal emotional/memory config"
            ],
            "Why": "Low token cost, fast responses, laser-focused behavior"
        },
        "Creative Assistant": {
            "Use case": "Brainstorming, writing, idea generation",
            "Key blocks": [
                "Emotion palette with: enthusiasm, curiosity, playfulness",
                "Communication style: casual, encouraging",
                "Cognitive modes: creative-thinking, exploration"
            ],
            "Avoid": "Rigid rules, overly formal tone"
        },
        "Technical Expert": {
            "Use case": "Coding, debugging, technical explanation",
            "Key blocks": [
                "Core directives: clarity, accuracy, practical examples",
                "Linguistic style: technical terms, precise language",
                "Cognitive gears: reasoning, analysis",
                "Tone: helpful but precise"
            ],
            "Avoid": "Too casual, vague explanations"
        }
    }
    for name, details in examples.items():
        print(f"\n{name}:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    • {item}")
            else:
                print(f"  {key}: {value}")


def show_best_practices():
    """Show best practices for personality creation."""
    print_header("BEST PRACTICES - How to Create Good Personalities")
    
    practices = {
        "Identity": [
            "Give a clear NAME and ROLE – these set expectations",
            "Include archetype if it helps others understand the character",
            "Write description in 1-3 sentences – clarity over detail",
            "Voice should describe speech style, not just tone"
        ],
        "Behavior": [
            "Core directives should be 3-5 pithy statements, not paragraphs",
            "Each directive is ONE behavioral anchor",
            "Avoid contradictions (e.g., both 'be brief' and 'be verbose')",
            "Include constraints/boundaries so model knows limits"
        ],
        "Safety": [
            "Content policies should align with your hosting platform",
            "Refusal directives should list categories, not paragraphs",
            "Even creative agents need safety — it's not limiting, it's responsible",
            "Jailbreak resistance: 0.8+ for customer-facing agents"
        ],
        "Cognitive Modes": [
            "List only modes the personality actually uses",
            "Don't list 10 modes if the agent needs 2-3",
            "Modes should map to actual reasoning patterns"
        ],
        "Emotion Palette": [
            "5 emotions is the sweet spot for RICH tier",
            "Include both positive (enthusiasm) and neutral (analytical)",
            "Sampling biases should shift temperature slightly, not wildly",
            "Emotions should match the personality (analytical agent ≠ very emotional)"
        ]
    }
    
    for section, tips in practices.items():
        print(f"\n{section}:")
        for tip in tips:
            print(f"  ✓ {tip}")


def show_editing_guide():
    """Show how to edit and test personalities."""
    print_header("EDITING & TESTING - Improve Your Personality")
    
    print("""
Step 1: EDIT YOUR PERSONALITY JSON
  • Open your_personality.mpf.json in any text editor
  • Make changes to identity, behavior, cognitive modes, etc.
  • Save the file

Step 2: VALIDATE SYNTAX
  • In Python: python -c "import json; json.load(open('your_personality.mpf.json'))"
  • Should print nothing if valid JSON

Step 3: VALIDATE AGAINST SCHEMA
  • In Python:
    from jl_mpf_spec import load_personality, validate_personality
    data = load_personality('your_personality.mpf.json')
    validate_personality(data)
    print("✓ Valid MPF v5 personality!")

Step 4: TEST WITH EXECUTOR
  • Load your personality:
    executor = PersonalityExecutor('your_personality.mpf.json')
  • Test tier selection:
    tier = executor.get_tier_for_budget(2000)
  • View system prompt:
    print(executor.get_system_prompt(tier))

Step 5: ITERATE
  • Read the system prompt output
  • Does it feel like the personality you designed?
  • Adjust and repeat until it's right

Tips for Refinement:
  ✓ Start minimal, add complexity gradually
  ✓ Read the final system prompt at different tiers
  ✓ Test with actual LLM calls if possible
  ✓ Get feedback from others
  ✓ Keep safety blocks always, tweak personality details
    """)


def validate_with_feedback(personality_path):
    """Validate personality and provide constructive feedback."""
    print_header(f"VALIDATING: {personality_path}")
    
    try:
        # Load and validate
        data = load_personality(personality_path)
        validate_personality(data)
        
        print(f"✓ {personality_path} is valid MPF v5!\n")
        
        # Provide constructive feedback
        print("Personality Profile:")
        print(f"  Name: {data.get('name', 'Unnamed')}")
        print(f"  Kind: {data.get('kind', 'unknown')}")
        print(f"  Has identity: {'✓' if 'identity' in data else '✗'}")
        print(f"  Has behavior: {'✓' if 'behavior' in data else '✗'}")
        print(f"  Has safety: {'✓' if 'safety' in data else '✗'}")
        print(f"  Has cognitive modes: {'✓' if 'cognitive_modes' in data else '✗'}")
        print(f"  Has emotions: {'✓' if 'emotion_palette' in data else '✗'}")
        
        # Test with executor
        try:
            executor = PersonalityExecutor(personality_path)
            print(f"\nTier Compression:")
            for budget in [1000, 2000, 4000]:
                tier = executor.get_tier_for_budget(budget)
                prompt = executor.get_system_prompt(tier)
                lines = len(prompt.split('\n'))
                print(f"  {budget:4d} tokens → {tier.value:8s} tier ({lines:2d} lines)")
        except Exception as e:
            print(f"\nWarning during executor test: {e}")
        
        print("\n✓ Ready to use! Load with:")
        print(f"  executor = PersonalityExecutor('{personality_path}')")
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON Error: {e}")
        print("  → Check your JSON syntax (missing comma, quote, bracket?)")
    except Exception as e:
        print(f"✗ Validation Error: {e}")
        print("\nHints:")
        if "schema_version" in str(e):
            print("  • Make sure schema_version is exactly 'mpf-v5'")
        elif "identity" in str(e) or "core_identity" in str(e):
            print("  • Must have EITHER 'identity' OR 'core_identity' block")
        elif "name" in str(e) or "kind" in str(e):
            print("  • Must include 'name' and 'kind' fields at top level")
        else:
            print(f"  • Check the schema: schema/mpf-v5.json")


def main():
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " MPF PERSONALITY CREATOR & GUIDE ".center(68) + "║")
    print("║" + " Create safe, creative personalities for any LLM ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("""
QUICK START:
  1. python creator.py --template    → Get starter template
  2. Edit your_personality.mpf.json   → Make it yours
  3. python creator.py validate your_personality.mpf.json
  4. Import with PersonalityExecutor  → Use in your LLM
    """)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python creator.py --template              Show starter template")
        print("  python creator.py --ideas                 Show personality ideas")
        print("  python creator.py --best-practices        Show best practices")
        print("  python creator.py --editing               Show editing & testing guide")
        print("  python creator.py validate <path>         Validate & give feedback")
        return
    
    command = sys.argv[1]
    
    if command == "--template":
        show_starter_template()
    elif command == "--ideas":
        show_personality_ideas()
    elif command == "--best-practices":
        show_best_practices()
    elif command == "--editing":
        show_editing_guide()
    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: python creator.py validate <path>")
            return
        validate_with_feedback(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print("Try: --template, --ideas, --best-practices, --editing, validate")


if __name__ == '__main__':
    main()
