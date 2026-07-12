#!/usr/bin/env python3
"""Fable-5 Orchestrator: Build a world map dashboard."""
import sys, os, time
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
PROJECT_DIR = Path(__file__).resolve().parent / "global-cyber-threat-map"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig, Orchestrator
from fable_agent.memory import create_memory

config = FableConfig.load(
    workspace=str(PROJECT_DIR),
    provider="openai-compatible", model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/v1",
    max_iterations=25, max_delegations=10,
)
config.api_key = os.environ.get("DEEPSEEK_API_KEY")
memory = create_memory(config.memory_backend, config.memory_path)

def hook(agent, event, detail):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] [{agent}/{event}] {str(detail)[:130]}", flush=True)

orchestrator = Orchestrator(config=config, memory=memory, on_event=hook)

task = """Read data.json in the workspace. Build a self-contained index.html:
World map dashboard using Leaflet.js CDN + Chart.js CDN + dark theme.
- Map with circle markers at each country lat/lng, colored by threatLevel
  (red=Critical, orange=High, yellow=Medium)
- Click popups showing country name, breach count, score, avg cost
- Top: 4 KPI cards (total breaches, total ransomware, highest threat country,
  average breach cost)
- Bar chart: threat types by incidents
- Line chart: monthly incident trend
- Sortable data table of all countries
- Dark theme (#0f172a bg, amber #f59e0b accent)
Delegate to Architect first to read data.json and plan.
Then delegate to Coder to write index.html with write_file.
Then delegate to Verifier to check it works."""

print(f"[{time.strftime('%H:%M:%S')}] FABLE-5 ORCHESTRATOR STARTING", flush=True)
t0 = time.time()
try:
    result = orchestrator.run_task(task)
    elapsed = time.time() - t0
    print(f"\n[{time.strftime('%H:%M:%S')}] DONE: {elapsed:.0f}s, success={result.success}, iters={result.iterations}", flush=True)
    print(result.output[:1000], flush=True)
except Exception as e:
    print(f"ERROR after {time.time()-t0:.0f}s: {e}", flush=True)
