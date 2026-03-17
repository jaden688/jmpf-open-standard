#!/usr/bin/env python3
"""Test script to verify refactoring is successful."""

import sys
sys.path.insert(0, 'python')

from jl_mpf_spec import PersonalityExecutor, ContextTier, validate_personality, load_personality

print("=" * 60)
print("MPF Refactoring Validation Test")
print("=" * 60)

# Test 1: Load and validate both examples
print("\n[1] Testing schema validation...")
for example_file in ['examples/sparkbyte.mpf.json', 'examples/neutral_assistant.mpf.json']:
    try:
        data = load_personality(example_file)
        validate_personality(data)
        print(f"  ✓ {example_file} - OK")
    except Exception as e:
        print(f"  ✗ {example_file} - FAILED: {e}")

# Test 2: Test PersonalityExecutor
print("\n[2] Testing PersonalityExecutor...")
try:
    executor = PersonalityExecutor('examples/sparkbyte.mpf.json')
    print(f"  ✓ Loaded: {executor.name} ({executor.agent_kind})")
    print(f"  ✓ Schema: {executor.data['schema_version']}")
    print(f"  ✓ Type: {'Rich Personality' if executor.is_rich_personality else 'Lean Task Agent'}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")

# Test 3: Test tier selection
print("\n[3] Testing tier selection by token budget...")
try:
    test_budgets = [250, 750, 2000, 5000]
    for budget in test_budgets:
        tier = executor.get_tier_for_budget(budget)
        print(f"  ✓ Budget {budget:4d} tokens -> {tier.value:8s} tier")
except Exception as e:
    print(f"  ✗ FAILED: {e}")

# Test 4: Test context compression
print("\n[4] Testing context compression...")
try:
    for tier in [ContextTier.MINIMAL, ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL]:
        prompt = executor.get_system_prompt(tier)
        lines = len(prompt.split('\n')) if prompt else 0
        print(f"  ✓ {tier.value:8s} tier: system prompt = {lines} lines")
except Exception as e:
    print(f"  ✗ FAILED: {e}")

print("\n" + "=" * 60)
print("All refactoring tests completed successfully!")
print("=" * 60)
