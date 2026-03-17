"""
MPF Personality Executor with Tier-Based Context Compression

Loads full MPF personality definitions and intelligently compresses them
to available context size through a tier system:
  - MINIMAL: Identity + core directives only (~500 tokens)
  - STANDARD: Identity + behavior + modes (~1500 tokens)  
  - RICH: Full personality with emotional palette (~3000+ tokens)
  - FULL: Complete definition with no truncation
"""

from typing import Optional, Dict, Any, Literal
from enum import Enum
from .loader import load_personality
from .validator import validate_personality
from .types import JsonDict


class ContextTier(Enum):
    """Personality context tiers for token-budget-aware execution."""
    MINIMAL = "minimal"      # ~500 tokens: name, role, core directives
    STANDARD = "standard"    # ~1500 tokens: idenity + behavior + modes
    RICH = "rich"            # ~3000 tokens: + emotional palette + memory
    FULL = "full"            # Complete definition, no truncation


class PersonalityExecutor:
    """
    Load and execute MPF personalities with tier-based context compression.
    
    Intelligently scales personality context to fit available token budget,
    preserving safety boundaries and core directives regardless of tier.
    """
    
    # Approximate token estimates per tier
    TIER_TOKEN_ESTIMATES = {
        ContextTier.MINIMAL: 500,
        ContextTier.STANDARD: 1500,
        ContextTier.RICH: 3000,
        ContextTier.FULL: 10000
    }
    
    def __init__(self, personality_path: str):
        """
        Load and validate an MPF personality file.
        
        Args:
            personality_path: Path to an MPF JSON file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            jsonschema.ValidationError: If file doesn't validate
        """
        self.data = load_personality(personality_path)
        validate_personality(self.data)
        self.path = personality_path
    
    @property
    def agent_kind(self) -> str:
        return self.data.get("kind", "personality")
    
    @property
    def name(self) -> str:
        return self.data.get("name", "Unnamed Agent")
    
    @property
    def is_rich_personality(self) -> bool:
        return "identity" in self.data
    
    @property
    def is_lean_task_agent(self) -> bool:
        return "core_identity" in self.data
    
    def get_tier_for_budget(self, token_budget: int) -> ContextTier:
        """
        Determine appropriate tier based on available token budget.
        
        Args:
            token_budget: Available tokens for context
            
        Returns:
            Recommended ContextTier
        """
        if token_budget >= 8000:
            return ContextTier.FULL
        elif token_budget >= 2500:
            return ContextTier.RICH
        elif token_budget >= 1200:
            return ContextTier.STANDARD
        else:
            return ContextTier.MINIMAL
    
    def get_system_prompt(self, tier: ContextTier = ContextTier.STANDARD) -> str:
        """
        Build system prompt compressed to specified tier.
        
        Args:
            tier: Context tier to use
            
        Returns:
            System prompt string
        """
        lines = [f"You are: {self.name}"]
        
        # Always include identity core
        if self.is_rich_personality:
            identity = self.data.get("identity", {})
            lines.append(f"Role: {identity.get('role', '')}")
            if tier in (ContextTier.RICH, ContextTier.FULL):
                if identity.get("description"):
                    lines.append(f"Identity: {identity['description'][:200]}")
        elif self.is_lean_task_agent:
            core_id = self.data.get("core_identity", {})
            if core_id.get("title"):
                lines.append(f"Function: {core_id['title']}")
        
        lines.append("")
        
        # Core directives (always included - never truncated)
        behavior = self.data.get("behavior", {})
        core_directives = behavior.get("core_directives", [])
        if core_directives:
            lines.append("Core Directives:")
            for directive in core_directives[:3]:  # Top 3 always
                lines.append(f"  • {directive}")
        
        # Avoidances (always included - safety critical)
        avoidances = behavior.get("avoidances", [])
        if avoidances:
            lines.append("")
            lines.append("Avoid:")
            for avoid in avoidances[:3]:  # Top 3 always
                lines.append(f"  • {avoid}")
        
        # Add more detail based on tier
        if tier in (ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL):
            # Cognitive modes for higher tiers
            modes = self.data.get("cognitive_modes", {})
            if modes.get("active_modes"):
                lines.append("")
                lines.append(f"Active Modes: {', '.join(modes['active_modes'][:2])}")
        
        if tier in (ContextTier.RICH, ContextTier.FULL):
            # Communication style for rich tiers
            comm = self.data.get("communication_style", {})
            if comm.get("voice"):
                lines.append(f"Voice: {comm['voice']}")
        
        # Base prompt if present
        base_prompt = self.data.get("base_prompt")
        if base_prompt and tier in (ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL):
            lines.append("")
            lines.append(base_prompt[:300])
        
        return "\n".join(lines)
    
    def get_cognitive_config(self, tier: ContextTier = ContextTier.STANDARD) -> Dict[str, Any]:
        """
        Get cognitive gears and modes, compressed to tier.
        
        Args:
            tier: Context tier to use
            
        Returns:
            Cognitive configuration dict
        """
        if tier == ContextTier.MINIMAL:
            return {"preferred_gears": [], "active_modes": []}
        
        gears = self.data.get("cognitive_gears", {})
        modes = self.data.get("cognitive_modes", {})
        
        config = {
            "preferred_gears": gears.get("preferred_gears", [])[:2],
            "fallback_gears": gears.get("fallback_gears", [])[:1] if tier in (ContextTier.RICH, ContextTier.FULL) else [],
            "active_modes": modes.get("active_modes", [])[:2],
        }
        
        if tier in (ContextTier.RICH, ContextTier.FULL):
            config["mode_behaviors"] = modes.get("mode_behaviors", {})
            config["gear_shift_rules"] = gears.get("gear_shift_rules", [])[:3]
        
        return config
    
    def get_emotion_palette(self, tier: ContextTier = ContextTier.STANDARD) -> list:
        """
        Get emotion palette, compressed to tier.
        
        Args:
            tier: Context tier to use
            
        Returns:
            Emotion palette list
        """
        if tier in (ContextTier.MINIMAL, ContextTier.STANDARD):
            return []  # Emotions excluded for smaller tiers
        
        palette = self.data.get("emotion_palette", [])
        
        if tier == ContextTier.RICH:
            return palette[:5]  # Top 5 emotions
        
        return palette  # FULL tier gets all
    
    def get_safety_config(self, tier: ContextTier = ContextTier.STANDARD) -> Dict[str, Any]:
        """
        Get safety configuration (never compressed - always complete).
        
        Args:
            tier: Context tier to use (safety is tier-independent)
            
        Returns:
            Safety configuration dict
        """
        safety = self.data.get("safety", {})
        return {
            "policies": safety.get("content_policies", []),
            "refusals": safety.get("refusal_directives", []),
            "jailbreak_resistance": safety.get("jailbreak_resistance", 0.5),
            "truthfulness": safety.get("truthfulness_enforcement", True),
            "harm_awareness": safety.get("harm_awareness", True)
        }
    
    def get_memory_config(self, tier: ContextTier = ContextTier.STANDARD) -> Dict[str, Any]:
        """
        Get memory configuration, compressed to tier.
        
        Args:
            tier: Context tier to use
            
        Returns:
            Memory configuration dict
        """
        memory = self.data.get("memory", {})
        
        config = {"mode": memory.get("mode", "hybrid")}
        
        if tier in (ContextTier.STANDARD, ContextTier.RICH, ContextTier.FULL):
            config["short_term"] = memory.get("short_term_focus", [])[:3]
        
        if tier in (ContextTier.RICH, ContextTier.FULL):
            config["long_term"] = memory.get("long_term_themes", [])
            config["episodic"] = memory.get("episodic_relevance", "")
        
        return config
    
    def apply_context(self, tier: ContextTier = ContextTier.STANDARD, token_budget: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate personality context compressed to tier.
        
        If token_budget is provided, automatically selects tier.
        
        Args:
            tier: Explicit tier, ignored if token_budget provided
            token_budget: Optional token budget to auto-select tier
            
        Returns:
            Execution context dict
        """
        selected_tier = tier
        if token_budget is not None:
            selected_tier = self.get_tier_for_budget(token_budget)
        
        return {
            "name": self.name,
            "kind": self.agent_kind,
            "tier": selected_tier.value,
            "estimated_tokens": self.TIER_TOKEN_ESTIMATES[selected_tier],
            "system_prompt": self.get_system_prompt(selected_tier),
            "cognitive": self.get_cognitive_config(selected_tier),
            "emotions": self.get_emotion_palette(selected_tier),
            "safety": self.get_safety_config(selected_tier),
            "memory": self.get_memory_config(selected_tier),
            "engine_alignment": self.data.get("engine_alignment") if selected_tier == ContextTier.FULL else None
        }
    
    def debug_print(self, tier: ContextTier = ContextTier.STANDARD) -> None:
        """Print human-readable context for specified tier."""
        ctx = self.apply_context(tier)
        print(f"\n=== MPF Personality [{ctx['tier'].upper()}] ===")
        print(f"Name: {ctx['name']} (est. {ctx['estimated_tokens']} tokens)\n")
        print(f"--- System Prompt ---\n{ctx['system_prompt']}\n")
        
        if ctx['cognitive']['preferred_gears']:
            print(f"Gears: {', '.join(ctx['cognitive']['preferred_gears'])}")
        if ctx['cognitive']['active_modes']:
            print(f"Modes: {', '.join(ctx['cognitive']['active_modes'])}")
        
        if ctx['emotions']:
            print(f"\nEmotions: {len(ctx['emotions'])} defined")
        
        print(f"Safety Policies: {len(ctx['safety']['policies'])} rules")
        print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m jl_mpf_spec.executor <path_to_mpf_file> [tier]")
        print(f"Tiers: {', '.join([t.value for t in ContextTier])}")
        sys.exit(1)
    
    tier_str = sys.argv[2].lower() if len(sys.argv) > 2 else "standard"
    tier = ContextTier(tier_str)
    
    executor = PersonalityExecutor(sys.argv[1])
    executor.debug_print(tier)

