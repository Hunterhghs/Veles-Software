#!/usr/bin/env python3
"""Fable-5 Orchestrator test — enhance a report with market opportunity section."""
import sys, os, time
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
REPORT_DIR = Path(__file__).resolve().parent / "clean-cooking-report"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig, Orchestrator
from fable_agent.memory import create_memory

config = FableConfig.load(
    workspace=str(REPORT_DIR),
    provider="openai-compatible", model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/v1",
    max_iterations=15, max_delegations=6, command_timeout=30,
)
config.api_key = os.environ.get("DEEPSEEK_API_KEY")
memory = create_memory(config.memory_backend, config.memory_path)

def hook(agent, event, detail):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] [{agent}/{event}] {str(detail)[:130]}", flush=True)

orchestrator = Orchestrator(config=config, memory=memory, on_event=hook)

task = """The workspace has data.json (clean cooking market data) and build_report.py
(a report generator script). Read data.json, then enhance build_report.py to add
a new section called "Market Opportunity" that includes: (1) a summary of the total
addressable market, (2) key growth drivers from distribution models, (3) the carbon
finance opportunity.

Delegate to Architect first to plan the change, then Coder to implement it with
edit_file or write_file, then Verifier to test the updated script runs correctly.
Keep it focused and efficient."""

print(f"[{time.strftime('%H:%M:%S')}] ORCHESTRATOR STARTING", flush=True)
t0 = time.time()
try:
    result = orchestrator.run_task(task)
    elapsed = time.time() - t0
    print(f"\n[{time.strftime('%H:%M:%S')}] DONE: {elapsed:.0f}s, success={result.success}, iters={result.iterations}", flush=True)
    print(f"OUTPUT: {result.output[:600]}", flush=True)
    
    # Show memory
    print("\nMEMORY AFTER RUN:", flush=True)
    for e in memory.recent(limit=3):
        print(f"  [{e.category}] {e.content[:120]}...", flush=True)
except Exception as e:
    print(f"ERROR after {time.time()-t0:.0f}s: {e}", flush=True)
