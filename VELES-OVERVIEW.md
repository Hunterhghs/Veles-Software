# Veles — Hybrid AI Agent Pipeline

**Fable-5 × DeepSeek · Assembled in Reasonix · H Heuristics**

---

## What Is Veles

Veles is a hybrid AI agent program built from two components:

| Component | Role |
|-----------|------|
| **Fable-5** (Claude-origin, forked & customized) | Multi-agent framework: Orchestrator → Architect → Coder → Verifier → Memory |
| **DeepSeek API** (v4-pro) | Model provider powering all sub-agents and the orchestrator |
| **Reasonix** | Host environment — the shell where Veles lives and is invoked |

The result: an autonomous software engineering team that plans, builds, reviews, verifies, and remembers — all accessible with a single command from within Reasonix.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      R E A S O N I X                         │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                   V E L E S                          │   │
│   │                                                     │   │
│   │   ┌──────────────┐    ┌──────────────────────────┐  │   │
│   │   │   Fable-5    │◄───│     DeepSeek v4-pro      │  │   │
│   │   │   (fork)     │    │     (API provider)        │  │   │
│   │   │              │    └──────────────────────────┘  │   │
│   │   │ Orchestrator │                                   │   │
│   │   │      │       │    ┌──────────────────────────┐  │   │
│   │   │  ┌───┼───┐   │    │  Custom H Heuristics     │  │   │
│   │   │  │   │   │   │    │  Tools (3)               │  │   │
│   │   │  ▼   ▼   ▼   │    └──────────────────────────┘  │   │
│   │   │ Ar  Co  Ve   │                                   │   │
│   │   │             │    ┌──────────────────────────┐  │   │
│   │   │   Memory    │    │  Workflow Scripts (3)    │  │   │
│   │   │   (SQLite)  │    │  seed · architect · verify│  │   │
│   │   └─────────────┘    └──────────────────────────┘  │   │
│   │                                                     │   │
│   │   Commands: new · design · verify · run · memory    │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   Default mode: Reasonix + deepseek-v4-pro (creative work)  │
│   Veles invoked: on mention of "Veles" or explicit trigger  │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
python3 veles status          # Health check — all green?
python3 veles new <project>   # Bootstrap a new project
python3 veles design <path>   # Architect reviews code
python3 veles verify <path>   # Pre-push quality audit
python3 veles run <path> <t>  # Full autonomous pipeline
```

## Capabilities — What Veles Can Build

### Professional-Grade Websites
Multi-page or single-page sites with responsive design, dark/light themes, CDN-optimized. Economist aesthetic, system font stacks, zero-build deployment to Cloudflare Pages.
→ *Example: Cybersecurity Landscape Intelligence (4-tab SPA, Economist aesthetic)*

### Interactive World Map Dashboards
Folium-based or Chart.js-powered interactive maps with choropleth layers, regional drill-downs, KPI overlays, and data filtering. Publication-quality data visualization.
→ *Example: World Map of Economies (wme.hheuristics.com)*

### Market Intelligence Dashboards
Executive dashboards with KPI cards, bar/line/doughnut charts, sortable tables, regional breakdowns, investment analysis, and technology comparisons. Self-contained HTML, browser-openable.
→ *Example: Electric Cooking Market Intelligence Dashboard*

### Comprehensive Reports
Data-driven PDF reports (5+ pages) with title pages, executive summaries, data tables, policy recommendations, source attribution, and professional typography.
→ *Example: Clean Cooking Transition Report (5-page PDF)*

### Informational Microsites
Narrative-driven scrolling sites with hero sections, stat counters, chart visualizations, technology cards, timeline elements, and calls to action.
→ *Example: The Clean Cooking Transition (7-section narrative site)*

## The Pipeline — How Veles Works

Every Veles project follows the same three-phase pattern:

```
Phase 1: BOOTSTRAP
  veles new <project>              ← Creates directory, config, seeds memory
  [Reasonix builds the project]    ← Creative work, skill pipelines, full context

Phase 2: ENHANCE
  veles design <project> "query"   ← Architect reads code, proposes improvements
  [Reasonix implements changes]    ← Polish, expand, refine

Phase 3: SHIP
  veles verify <project>           ← Verifier audits: PASS/FAIL with evidence
  [Fix any FAIL items]             ← Targeted corrections
  git push                         ← Deploy to Cloudflare Pages
```

## Sub-Agent Roles

| Agent | Access | Purpose | Speed |
|-------|--------|---------|-------|
| **Orchestrator** | Delegates only | Plans task, delegates to sub-agents, summarizes results | 30–90s |
| **Architect** | Read-only | Explores codebase, proposes concrete improvements | 5–15s |
| **Coder** | Full R/W | Implements changes, writes files, runs commands | 5–30s |
| **Verifier** | Read + Execute | Audits quality, runs tests, returns PASS/FAIL | 10–30s |

## Invocation — When Veles Is Called

Veles is NOT the default. It is invoked explicitly when its capabilities are needed. In Reasonix, mentioning "Veles" or any of its trigger phrases activates the hybrid system.

**Invoke Veles for:**
- Code review and design audit
- Pre-push quality verification
- Project bootstrap and memory seeding
- Autonomous code generation for well-scoped tasks
- Enhancement planning (Architect analysis)

**Do NOT invoke Veles for:**
- Creative strategy and design decisions
- Full website/dashboard builds from scratch (Reasonix + skills handle these)
- Simple questions or explanations
- Multi-skill pipelines (accessibility, performance, design system)

## Configuration

Veles auto-detects `DEEPSEEK_API_KEY` from the Reasonix environment. No manual setup required. All configuration lives in `fable.toml`:

```toml
[fable]
provider = "openai-compatible"
model = "deepseek-v4-pro"
base_url = "https://api.deepseek.com/v1"
memory_backend = "sqlite"
```

## Files

| Path | Purpose |
|------|---------|
| `veles` | Unified CLI — single entry point for all commands |
| `Fable-5/` | Forked Fable Agent framework (v7905969) |
| `fable.toml` | Provider and model configuration |
| `fable-seed-memory.py` | Memory seeding for new projects |
| `fable-architect.py` | Architect sub-agent runner |
| `fable-verify.py` | Verifier sub-agent runner |
| `Fable-5/fable_agent/config.py` | Auto-detects DEEPSEEK_API_KEY |
| `Fable-5/fable_agent/tools/hheuristics.py` | 3 custom H Heuristics tools |

## Projects Built with Veles

| Project | Type | Repo |
|---------|------|------|
| Electric Cooking Market Intelligence | Dashboard | `Dashboard-electric-cooking-market` |
| Clean Cooking Transition | Informational Site | `clean-cooking-transition-informational-website` |
| Clean Cooking Report | PDF Report | `clean-cooking-report` |
| Cybersecurity Landscape Intelligence | 4-Tab SPA | `Informational-resource-on-cybersecurity` |
| World Map of Economies | Interactive Map | `wme.hheuristics.com` |

---

*Veles is maintained in `/Users/hunterhughes/.reasonix/global-workspace/`. All projects deploy to Cloudflare Pages. The pipeline is production-tested across dashboards, websites, reports, and interactive visualizations.*
