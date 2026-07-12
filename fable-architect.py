#!/usr/bin/env python3
"""Fable-5: Run Architect sub-agent on a project for design review.

Usage:
    cd global-workspace
    python3 fable-architect.py [workspace-path] ["optional custom question"]

Examples:
    python3 fable-architect.py Dashboard-electric-cooking-market
    python3 fable-architect.py . "How would you add comparative country benchmarks?"
"""

import sys, os, textwrap
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig
from fable_agent.agents.subagents import ArchitectAgent
from fable_agent.llm import create_provider

workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
workspace = workspace.resolve()
custom_question = sys.argv[2] if len(sys.argv) > 2 else None

config = FableConfig.load(workspace=str(workspace))
config.max_iterations = 15

# Auto-detect DEEPSEEK_API_KEY if not already set
if not config.api_key:
    config.api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("FABLE_API_KEY")
if not config.api_key:
    config.api_key = os.environ.get("DEEPSEEK_API_KEY")

provider = create_provider(config)
architect = ArchitectAgent(provider, config)

# Inject project memory as context
from fable_agent.memory import create_memory
memory_path = workspace / ".fable" / "memory"
try:
    mem = create_memory(config.memory_backend, memory_path)
    recent = mem.recent(limit=5)
    memory_context = None
    if recent:
        memory_context = "Project memory from previous sessions:\n" + "\n".join(
            f"- [{e.category}] {e.content}" for e in recent
        )
except Exception:
    memory_context = None

if custom_question:
    task = textwrap.dedent(f"""\
        Explore the workspace at {workspace}. Understand the project structure,
        key files, and codebase. Then answer this question:

        {custom_question}

        Be specific: name files, describe concrete changes, and note any risks.
    """)
else:
    task = textwrap.dedent(f"""\
        Explore the workspace at {workspace}. Understand the project structure.

        Produce:
        1. Context — summary of what this project is and how it's built.
        2. Quality assessment — what's working well, what could improve.
        3. Enhancement plan — 3 specific, actionable improvements with file
           names and concrete implementation guidance.

        Focus on analytical value, not cosmetic changes.
    """)

print(f"🏗️  Fable-5 Architect analyzing: {workspace.name}")
print(f"   Provider: {config.provider} | Model: {config.model}")
print(f"   API key: {'✅' if config.api_key else '❌ MISSING — set DEEPSEEK_API_KEY'}")
print()

if not config.api_key:
    sys.exit(1)

try:
    result = architect.run(task, context=memory_context)
    print(f"✅ Completed in {result.iterations} iteration(s)\n")
    print(result.output)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
