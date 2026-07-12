#!/usr/bin/env python3
"""Fable-5: Seed project memory with H Heuristics context.

Usage:
    cd global-workspace
    python3 fable-seed-memory.py [project-name] [workspace-path]

Examples:
    python3 fable-seed-memory.py electric-cooking Dashboard-electric-cooking-market
    python3 fable-seed-memory.py convergence-crisis convergence-crisis-site
    python3 fable-seed-memory.py                    # uses current dir as workspace
"""

import sys, os
from pathlib import Path

FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent.memory import create_memory

project_name = sys.argv[1] if len(sys.argv) > 1 else Path.cwd().name
workspace = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
workspace = workspace.resolve()
memory_path = workspace / ".fable" / "memory"
memory = create_memory("sqlite", memory_path)

# ── Standard H Heuristics project context ──
entries = [
    ("project-fact", "hheuristics-stack",
     f"H Heuristics technology stack for {project_name}: Chart.js for visualizations, "
     "Folium for interactive maps, Streamlit for data apps, Plotly for advanced charts, "
     "statsmodels for econometrics. Python 3.14.2. Prefer vanilla HTML/JS for dashboards, "
     "React+Vite for SPAs, self-contained HTML for Cloudflare Pages."),

    ("decision", "hheuristics-deploy",
     "All H Heuristics projects deploy to Cloudflare Pages as static sites. Use _headers "
     "file for security config. Zero build step for simple dashboards; Vite build for "
     "React SPAs. All sites are responsive, dark-themed, with Chart.js CDN visualizations."),

    ("decision", "hheuristics-quality",
     "Professional-grade, production-ready output required. Pixel-perfect responsive design, "
     "accessible (WCAG 2.1 AA target), fast-loading. System font stack (-apple-system, "
     "BlinkMacSystemFont, Segoe UI, Roboto). Dark slate (#0f172a) with amber accent (#f59e0b)."),

    ("project-fact", "hheuristics-data",
     f"Primary data sources for {project_name}: WHO, IEA, SEforALL, Clean Cooking Alliance, "
     "World Bank/ESMAP, Lancet Countdown. Data embedded as JavaScript const DATA in HTML; "
     "also available as data.json for reference. Sources cited in dashboard footer."),

    ("task", "hheuristics-active",
     f"Active development on {project_name} at {workspace}. Last updated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}. "
     "Use Fable-5 Architect for design review, Coder for targeted changes, "
     "Verifier for pre-push quality checks. Memory persists across sessions."),
]

for category, tags, content in entries:
    entry_id = memory.remember(content, category=category, tags=tags.split("-"))
    print(f"  ✓ [{category}] {content[:90]}...")

print(f"\n✅ {len(entries)} memories seeded for '{project_name}'")
print(f"   Memory store: {memory_path}")
print(f"   Total entries: {len(memory.recent(limit=20))}")
