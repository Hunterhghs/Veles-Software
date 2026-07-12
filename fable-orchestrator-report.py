#!/usr/bin/env python3
"""Full Fable-5 Orchestrator pipeline — clean cooking report.
Runs the complete autonomous pipeline: plan → Architect → Coder → Verifier → remember.
"""

import sys, os, time, textwrap
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
REPORT_DIR = Path(__file__).resolve().parent / "clean-cooking-report"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig, Orchestrator
from fable_agent.memory import create_memory

# ── Config ──
config = FableConfig.load(
    workspace=str(REPORT_DIR),
    provider="openai-compatible",
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/v1",
    max_iterations=25,
    max_delegations=10,
    command_timeout=60,
)
config.api_key = os.environ.get("DEEPSEEK_API_KEY")

# ── Progress hook ──
def on_event(agent: str, event: str, detail: str) -> None:
    icon = {"start": "🚀", "tool": "🔧", "finish": "✅", "budget_exhausted": "⚠️"}.get(event, "📌")
    if event == "tool":
        print(f"  {icon} [{agent}] {detail[:130]}")
    else:
        print(f"\n{icon} [{agent}] {event}: {detail[:200]}")

# ── Memory ──
memory = create_memory(config.memory_backend, config.memory_path)

# ── The task — focused, scoped, achievable ──
task = textwrap.dedent("""\
    Read data.json to understand the available data on the clean cooking transition.

    Your goal: produce a Python script called `build_report.py` that generates a
    professional 5-page PDF report on the clean cooking transition. The report should
    include:

    1. Title page with "The Clean Cooking Transition" and key stats
    2. Page on the human toll (2.9M deaths, disease breakdown)
    3. Page on the access gap by region
    4. Page on the climate connection (CO2 abatement, black carbon)
    5. Page on the path forward (investment needs, policy recommendations)

    How to work:
    - Delegate to ARCHITECT first to design the report structure and PDF generation approach
    - Then delegate to CODER to write build_report.py
    - Then delegate to VERIFIER to run the script and confirm the PDF was created
    - Use `remember` after each major step

    The Coder should use Python libraries already available (fpdf2 or reportlab are
    NOT guaranteed to be installed — use weasyprint or just write HTML-to-PDF via
    a simple approach, or generate a well-formatted markdown/text file as the report).
    Focus on making the CONTENT excellent and well-structured.

    The Coder MUST run the script after writing it to confirm it works.
""")

print("═" * 60)
print("🎯 FABLE-5 FULL ORCHESTRATOR — Clean Cooking Report")
print("═" * 60)
print(f"   Model: {config.model}")
print(f"   Workspace: {config.workspace}")
print(f"   Memory: {len(memory.recent(limit=20))} entries")
print(f"   Budget: {config.max_iterations} iters, {config.max_delegations} delegations")
print("═" * 60)

orchestrator = Orchestrator(config=config, memory=memory, on_event=on_event)

t0 = time.time()
try:
    result = orchestrator.run_task(task)
    elapsed = time.time() - t0
    print(f"\n{'═' * 60}")
    print(f"🏁 ORCHESTRATOR COMPLETE — {elapsed:.0f}s")
    print(f"   Success: {result.success}")
    print(f"   Iterations: {result.iterations}")
    print(f"{'═' * 60}")
    print(f"\n📋 Final Report:\n{result.output[:1000]}")
except Exception as e:
    elapsed = time.time() - t0
    print(f"\n❌ Error after {elapsed:.0f}s: {e}")

# ── Show memory after run ──
print(f"\n🧠 Memory after run:")
for entry in memory.recent(limit=5):
    print(f"   [{entry.category}] {entry.content[:120]}...")
