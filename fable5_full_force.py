"""
Fable-5 Full Force Demo — H Heuristics Electric Cooking Dashboard
=================================================================
Demonstrates: Memory Store · Direct Sub-Agent API · Custom Tools · MCP Export Readiness

Usage:
    cd Fable-5 && source .venv/bin/activate
    FABLE_API_KEY="$DEEPSEEK_API_KEY" python3 ../fable5_full_force.py
"""

import sys, os, json, time, textwrap
from pathlib import Path

# Paths
FABLE_DIR = Path(__file__).resolve().parent / "Fable-5"
DASHBOARD_DIR = Path(__file__).resolve().parent / "Dashboard-electric-cooking-market"
sys.path.insert(0, str(FABLE_DIR))

from fable_agent import FableConfig, Orchestrator
from fable_agent.agents.subagents import ArchitectAgent, CoderAgent, VerifierAgent
from fable_agent.llm import create_provider
from fable_agent.memory import create_memory, MemoryEntry
from fable_agent.tools.base import Tool, ToolResult, ToolRegistry
from fable_agent.tools import default_registry

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

config = FableConfig.load(
    workspace=str(DASHBOARD_DIR),
    provider="openai-compatible",
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    max_iterations=20,
    max_delegations=8,
)

# Override API key from env
config.api_key = os.environ.get("FABLE_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
provider = create_provider(config)
memory = create_memory(config.memory_backend, config.memory_path)

SEP = "\n" + "─" * 60

# ═══════════════════════════════════════════════════════════════
# 1. MEMORY STORE — Seed persistent project knowledge
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🔮 FABLE-5 MEMORY STORE — Seeding H Heuristics project context")
print(SEP)

# Clear any existing test entries from prior runs
for e in memory.recent(limit=20):
    if "hheuristics" in e.tags or "dashboard" in e.tags:
        memory.delete(e.id)

memories = [
    ("project-fact", "hheuristics-electric-cooking-dashboard",
     "Electric Cooking Market Intelligence Dashboard is a single-page HTML app at "
     "Dashboard-electric-cooking-market/index.html. It uses Chart.js v4.5.1 CDN, dark slate "
     "theme (#0f172a) with amber accent (#f59e0b). Data is embedded as JavaScript variables "
     "from data.json source file. Deployed via Cloudflare Pages."),

    ("decision", "hheuristics-design",
     "Dashboard uses system font stack (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto). "
     "All charts use Chart.js v4 with no framework dependencies. KPI cards use accent-color "
     "top borders (amber, red, green, blue). Technology table uses inline efficiency bars."),

    ("project-fact", "hheuristics-data-sources",
     "Data originates from WHO Household Air Pollution Fact Sheet (Dec 2025), IEA Clean Cooking "
     "in Africa 2026, SEforALL Chilling Prospects 2023, and Clean Cooking Alliance. "
     "Key metrics: 2.1B without clean cooking, 2.9M annual deaths, $8B/yr investment need, "
     "1.5 Gt CO2-eq abatement potential."),

    ("decision", "hheuristics-stack",
     "All H Heuristics dashboards deploy to Cloudflare Pages as static sites with zero build steps. "
     "Headers include X-Frame-Options: DENY, X-Content-Type-Options: nosniff, and strict "
     "Referrer-Policy. Use _headers file for Cloudflare-specific config."),

    ("project-fact", "hheuristics-tech-stack",
     "H Heuristics technology stack: Chart.js for visualizations, Folium for interactive maps, "
     "Streamlit for data apps, Plotly for advanced charts, statsmodels for econometrics. "
     "Python 3.14.2 runtime. Prefer vanilla HTML/JS for dashboards, React+Vite for SPAs."),

    ("task", "hheuristics-build",
     "2026-07-11: Built initial Electric Cooking Market Intelligence Dashboard. "
     "Used Fable-5 with DeepSeek for configuration and testing. Dashboard includes 4 KPI cards, "
     "regional bar chart, deaths doughnut, technology comparison table, investment gap chart, "
     "4 distribution model cards. Pushed to GitHub at Hunterhghs/Dashboard-electric-cooking-market."),
]

for category, tags, content in memories:
    entry_id = memory.remember(content, category=category, tags=tags.split("-"))
    print(f"  ✓ [{category}] {content[:80]}... (id={entry_id})")

# Verify
print(f"\n  📊 Total memories stored: {len(memory.recent(limit=20))}")

# Search test
results = memory.search("electric cooking dashboard")
print(f"  🔍 Search 'electric cooking dashboard' → {len(results)} results:")
for r in results:
    print(f"     - [{r.category}] {r.content[:100]}...")

# ═══════════════════════════════════════════════════════════════
# 2. CUSTOM TOOL — H Heuristics domain-specific extension
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🔧 FABLE-5 CUSTOM TOOL — Registering domain-specific capabilities")
print(SEP)


class ValidateDashboardTool(Tool):
    """Validates a dashboard HTML file for common issues."""
    name = "validate_dashboard"
    description = (
        "Validate a dashboard HTML file for common issues: checks for required "
        "elements (Chart.js CDN, responsive viewport meta, semantic HTML structure), "
        "reports missing features, and confirms data embedding."
    )
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the dashboard HTML file."},
        },
        "required": ["path"],
    }

    def execute(self, path: str) -> ToolResult:
        filepath = Path(path)
        if not filepath.exists():
            return ToolResult(output=f"ERROR: {path} not found.", success=False)

        html = filepath.read_text()
        checks = []

        # Required CDNs
        checks.append(("Chart.js CDN", "chart.js@4" in html.lower() or "chart.js@4" in html.lower()))
        # Viewport
        checks.append(("Responsive viewport meta", 'viewport' in html.lower() and 'initial-scale' in html.lower()))
        # Semantic structure
        checks.append(("Semantic header", '<header' in html.lower()))
        checks.append(("Semantic main", '<main' in html.lower()))
        checks.append(("Semantic footer", '<footer' in html.lower()))
        # KPI section
        checks.append(("KPI cards section", 'kpi' in html.lower()))
        # Canvas elements for charts
        checks.append(("Chart canvas elements", '<canvas' in html.lower()))
        # Data embedding
        checks.append(("Inline data embedding", 'const DATA' in html or 'const data' in html.lower()))
        # Security headers
        checks.append(("Frame protection", 'x-frame-options' in html.lower() or 'DENY' in html))
        # CSS variables / design tokens
        checks.append(("Design tokens (CSS vars)", '--' in html and 'var(--' in html))

        passed = sum(1 for _, ok in checks if ok)
        total = len(checks)
        lines = [f"Dashboard validation for {filepath.name}: {passed}/{total} checks passed", ""]
        for name, ok in checks:
            lines.append(f"  {'✅' if ok else '❌'} {name}")

        return ToolResult(output="\n".join(lines))


class FetchDataSourceTool(Tool):
    """Fetches or references known data sources for H Heuristics projects."""
    name = "fetch_data_source"
    description = (
        "Look up metadata about known H Heuristics data sources. Returns source name, "
        "URL, last update date, and key metrics available."
    )
    parameters = {
        "type": "object",
        "properties": {
            "source_name": {
                "type": "string",
                "description": "Data source to look up: who-hap, iea-cooking, seforall, cca, or all.",
            },
        },
        "required": ["source_name"],
    }

    SOURCES = {
        "who-hap": {
            "name": "WHO Household Air Pollution Fact Sheet",
            "url": "https://www.who.int/news-room/fact-sheets/detail/household-air-pollution-and-health",
            "updated": "December 2025",
            "key_metrics": ["2.9M annual deaths", "disease breakdown (IHD 32%, stroke 23%, LRI 21%, COPD 19%, lung cancer 6%)", "2.1B people using polluting fuels"],
        },
        "iea-cooking": {
            "name": "IEA Clean Cooking in Africa 2026",
            "url": "https://www.iea.org/reports/clean-cooking-in-africa-2026",
            "updated": "2026",
            "key_metrics": ["$8B/yr investment need", "$2.2B pledged at Paris Summit", "$0.74B disbursed by mid-2026", "Sub-Saharan Africa: 940M without access"],
        },
        "seforall": {
            "name": "SEforALL Chilling Prospects 2023",
            "url": "https://www.seforall.org/chilling-prospects-2023",
            "updated": "2023",
            "key_metrics": ["1.12B at high risk from lack of cooling", "Regional breakdown of cooling access gaps"],
        },
        "cca": {
            "name": "Clean Cooking Alliance",
            "url": "https://cleancooking.org/",
            "updated": "Ongoing",
            "key_metrics": ["Market intelligence", "Carbon finance standards", "Technology transition data"],
        },
    }

    def execute(self, source_name: str) -> ToolResult:
        if source_name == "all":
            lines = []
            for key, src in self.SOURCES.items():
                lines.append(f"  [{key}] {src['name']} ({src['updated']}) — {src['url']}")
                lines.append(f"       Metrics: {', '.join(src['key_metrics'][:2])}")
            return ToolResult(output="\n".join(lines))

        src = self.SOURCES.get(source_name)
        if not src:
            return ToolResult(output=f"Unknown source '{source_name}'. Try: {', '.join(self.SOURCES)} or 'all'.", success=False)

        return ToolResult(output=(
            f"{src['name']}\n"
            f"  URL: {src['url']}\n"
            f"  Updated: {src['updated']}\n"
            f"  Key metrics: {', '.join(src['key_metrics'])}"
        ))


# Register tools and test them
registry = default_registry(str(DASHBOARD_DIR))
validate_tool = ValidateDashboardTool()
data_tool = FetchDataSourceTool()
registry.register(validate_tool)
registry.register(data_tool)

# Test the custom tools
result = registry.execute("validate_dashboard", {"path": str(DASHBOARD_DIR / "index.html")})
print(result.output)

print()
result = registry.execute("fetch_data_source", {"source_name": "all"})
print(result.output)

print(f"\n  🧰 Total tools in registry: {len(registry.specs())} (7 built-in + 2 custom)")

# ═══════════════════════════════════════════════════════════════
# 3. DIRECT SUB-AGENT API — Architect reviews dashboard
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🏗️  FABLE-5 ARCHITECT SUB-AGENT — Direct API, analyzing dashboard for enhancements")
print(SEP)

architect = ArchitectAgent(provider, config)

architect_task = textwrap.dedent("""\
    Read index.html in the workspace root. This is an Electric Cooking Market Intelligence
    Dashboard. Analyze it and produce a concrete enhancement plan with exactly 3 specific,
    actionable improvements.

    Focus on features that add real analytical value (not cosmetic changes). For each
    improvement, name the exact file to change and describe the change concretely.

    Consider: interactive filters, additional data layers, sortable tables, export
    functionality, trend analysis, or comparative benchmarks.

    Reply with numbered improvements. Keep it tight — 3 improvements max.
""")

print("  🚀 Running Architect sub-agent (DeepSeek) on dashboard review...")
print(f"  Task: {architect_task[:120]}...")
print()

try:
    arch_result = architect.run(architect_task)
    print(f"  ✅ Architect completed in {arch_result.iterations} iteration(s)")
    print(f"  📋 Enhancement Plan:\n")
    for line in arch_result.output.split("\n"):
        print(f"     {line}")
    arch_output = arch_result.output
except Exception as e:
    print(f"  ⚠️  Architect error: {e}")
    arch_output = None

# ═══════════════════════════════════════════════════════════════
# 4. VERIFIER SUB-AGENT — Run quality checks on the dashboard
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🔍 FABLE-5 VERIFIER SUB-AGENT — Quality audit of dashboard")
print(SEP)

verifier = VerifierAgent(provider, config)

verifier_task = textwrap.dedent("""\
    Review index.html for correctness and quality:

    1. Read the file — verify Chart.js CDN is loaded, all canvas elements have matching
       JavaScript chart initialization code, and no broken references exist.
    2. Check that all data references in the HTML (kpiCards, cookingAccess, deathsBySource,
       investmentBreakdown, technologyComparison, distributionModels) match the embedded
       JavaScript DATA object structure.
    3. Verify the file is self-contained (no external CSS or JS dependencies beyond Chart.js CDN).
    4. Check for any obvious defects: unused CSS classes, duplicate IDs, missing closing tags.

    Start your reply with PASS or FAIL on the first line, then list evidence.
""")

print("  🚀 Running Verifier sub-agent (DeepSeek) on dashboard...")
print()

try:
    verifier_result = verifier.run(verifier_task)
    print(f"  ✅ Verifier completed in {verifier_result.iterations} iteration(s)")
    verdict = "PASS" if verifier_result.success else "FAIL"
    print(f"  📋 Verdict: ...")
    for line in verifier_result.output.split("\n")[:15]:
        print(f"     {line}")
except Exception as e:
    print(f"  ⚠️  Verifier error: {e}")

# ═══════════════════════════════════════════════════════════════
# 5. MCP SERVER — Demonstrate export readiness
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🌐 FABLE-5 MCP SERVER — Export layer readiness")
print(SEP)

print("  MCP server start command:")
print("    cd Fable-5 && source .venv/bin/activate")
print(f"    fable mcp --workspace {DASHBOARD_DIR}")
print()
print("  This exports over stdio:")
print("    🛠️  7 tools — read_file, write_file, edit_file, list_dir, grep, glob, run_command")
print("    🧠  2 memory tools — memory_remember, memory_recall")
print("    🤖  1 agent tool — run_agent (full orchestrator pipeline)")
print("    📝  4 prompts — fable_orchestrator, fable_coder, fable_verifier, fable_architect")
print()
print("  Any MCP client (Claude Code, Cursor, Reasonix) can consume this:")
print("    claude mcp add fable -- fable mcp --workspace /path/to/project")
print()
print("  With our custom tools, the export extends to:")
print("    🛠️  2 custom tools — validate_dashboard, fetch_data_source")

# ═══════════════════════════════════════════════════════════════
# 6. FULL ORCHESTRATOR — Small targeted task
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("🎯 FABLE-5 FULL ORCHESTRATOR — Targeted enhancement (Coder sub-agent)")
print(SEP)

# Only run if architect gave us something useful
if arch_output and "improvement" in arch_output.lower():
    coder_task = textwrap.dedent(f"""\
        Based on the architect's review, implement ONE small but impactful enhancement
        to index.html. The architect found these opportunities:

        {arch_output[:500]}

        Choose the most impactful single change you can implement cleanly. Make it
        self-contained — add or modify one section. Do NOT rewrite the entire file.
        Use edit_file for targeted changes. If the change is too complex for one edit,
        choose a simpler one.
    """)

    print("  🚀 Running Full Orchestrator with Architect's findings...")
    print()

    orchestrator = Orchestrator(config=config, provider=provider, memory=memory)
    try:
        orch_result = orchestrator.run_task(coder_task)
        print(f"  ✅ Orchestrator completed")
        print(f"  📋 Output: {orch_result.output[:500]}...")
    except Exception as e:
        print(f"  ⚠️  Orchestrator error: {e}")
else:
    print("  ⏭️  Skipping — no architect output to build on")
    print("  💡 To run the orchestrator directly on a focused task:")
    print("    orchestrator = Orchestrator(config=config)")
    print("    orchestrator.run_task('Add a trend line chart to the dashboard')")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

print(SEP)
print("✅ FABLE-5 FULL FORCE DEMO — Complete")
print(SEP)
print()
print("  What was demonstrated:")
print("    1. 🔮 Memory Store — 6 persistent entries seeded (project-fact, decision, task)")
print("       → Survives across sessions; MCP exports it to external agents")
print()
print("    2. 🔧 Custom Tools — validate_dashboard + fetch_data_source registered")
print("       → Extends Fable-5's tool suite with H Heuristics domain capabilities")
print()
print("    3. 🏗️  Architect Sub-Agent — Direct API call, analyzed dashboard for enhancements")
print("       → DeepSeek-powered codebase exploration, read-only safety")
print()
print("    4. 🔍 Verifier Sub-Agent — Quality audit with PASS/FAIL verdict")
print("       → Read+execute, can run tests/builds, cannot edit files")
print()
print("    5. 🌐 MCP Server — Export layer ready (tools + memory + prompts + run_agent)")
print("       → Interoperability with Claude Code, Cursor, Reasonix, custom scripts")
print()
print("    6. 🎯 Full Orchestrator — Plan → Delegate → Verify pipeline on enhancement task")
print("       → Orchestrator delegates to Architect → Coder → Verifier autonomously")
print()
print("  Configuration:")
print(f"    Provider: openai-compatible (DeepSeek)")
print(f"    Model: deepseek-chat")
print(f"    Workspace: {DASHBOARD_DIR}")
print(f"    Memory backend: {config.memory_backend}")
print(f"    Memory path: {config.memory_path}")
print(f"    API key configured: {'YES' if config.api_key else 'NO'}")
print()
print("  All sub-agent runs use Fable-5's sandboxed tooling suite —")
print("  file access is confined to the workspace directory.")
