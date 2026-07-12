#!/usr/bin/env python3
"""Fable-5: Run Verifier sub-agent for pre-push quality check."""
import sys, os, textwrap
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig
from fable_agent.agents.subagents import VerifierAgent
from fable_agent.llm import create_provider
from fable_agent.memory import create_memory

args = sys.argv[1:]
focus = None
workspace_arg = None
i = 0
while i < len(args):
    if args[i] == "--focus" and i + 1 < len(args):
        focus = args[i + 1]; i += 2
    elif workspace_arg is None:
        workspace_arg = args[i]; i += 1
    else:
        i += 1

workspace = Path(workspace_arg) if workspace_arg else Path.cwd()
workspace = workspace.resolve()

config = FableConfig.load(workspace=str(workspace))
config.max_iterations = 12

if not config.api_key:
    config.api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("FABLE_API_KEY")

provider = create_provider(config)
verifier = VerifierAgent(provider, config)

# Load project memory
memory_path = workspace / ".fable" / "memory"
memory_context = None
try:
    mem = create_memory(config.memory_backend, memory_path)
    recent = mem.recent(limit=5)
    if recent:
        lines = []
        for e in recent:
            lines.append(f"- [{e.category}] {e.content}")
        memory_context = "Project memory:\n" + "\n".join(lines)
except Exception:
    pass

if focus:
    task = f"Review the workspace at {workspace} with this specific focus:\n\n{focus}\n\nRead files, run commands if needed. Start with PASS or FAIL, then give evidence."
else:
    task = f"Review the workspace at {workspace} for correctness and quality. Start with PASS or FAIL, then list evidence."

print(f"Veles Verifier auditing: {workspace.name}")
print(f"   Provider: {config.provider} | Model: {config.model}")
if focus: print(f"   Focus: {focus}")
print()

try:
    result = verifier.run(task, context=memory_context)
    print(f"Completed in {result.iterations} iteration(s)\n")
    print(result.output)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
