# Veles Software

**Hybrid AI Agent Pipeline — Fable-5 × DeepSeek · H Heuristics**

Veles is a multi-agent AI framework for autonomous software engineering. It combines the Fable-5 orchestration engine with DeepSeek's API to plan, build, review, verify, and remember.

## Architecture

```
Orchestrator → Architect → Coder → Verifier → Memory (SQLite)
```

## Quick Start

```bash
python3 veles status          # Health check
python3 veles new <project>   # Bootstrap a new project
python3 veles design <path>   # Architect design review
python3 veles verify <path>   # Pre-push quality audit
python3 veles run <path> <t>  # Full autonomous pipeline
```

## Components

| Path | Purpose |
|------|---------|
| `veles` | Unified CLI — single entry point |
| `Fable-5/` | Multi-agent framework (git submodule → [Hunterhghs/Veles](https://github.com/Hunterhghs/Veles)) |
| `fable.toml` | Provider and model configuration |
| `fable-*.py` | Workflow scripts (architect, verify, seed, orchestrate) |
| `fable5_full_force.py` | Full end-to-end capability demo |
| `VELES-OVERVIEW.md` | Canonical documentation |
| `AGENTS.md` | Skill pipeline guide (50+ skills) |

## Configuration

Veles auto-detects `DEEPSEEK_API_KEY` from the environment. All config in `fable.toml`:

```toml
[fable]
provider = "openai-compatible"
model = "deepseek-v4-pro"
base_url = "https://api.deepseek.com/v1"
memory_backend = "sqlite"
```

## Cloning

```bash
git clone --recurse-submodules https://github.com/Hunterhghs/Veles-Software.git
```

---

*Maintained by H Heuristics. Production-tested across dashboards, websites, reports, and interactive visualizations.*
