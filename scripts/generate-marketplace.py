#!/usr/bin/env python3
"""Generate MARKETPLACE.md from the three marketplace catalogs."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads(pathlib.Path(p).read_text())

codex = load(ROOT / ".agents/plugins/marketplace.json")
claude = load(ROOT / ".claude-plugin/marketplace.json") if (ROOT / ".claude-plugin/marketplace.json").exists() else None
grok = load(ROOT / ".grok-plugin/marketplace.json") if (ROOT / ".grok-plugin/marketplace.json").exists() else None

plugins = codex.get("plugins", [])
# Use codex list as canonical table; fallback to claude/grok if needed
out = []
out.append("# FYQ Agent Plugins — Marketplace")
out.append("")
out.append("> Auto-generated from marketplace catalogs — do not hand-edit. Edit the catalog JSONs and run `python scripts/generate-marketplace.py`.")
out.append("")
out.append("This repo is a triple marketplace for **Codex** (`.agents/plugins/marketplace.json`), **Claude Code** (`.claude-plugin/marketplace.json`), and **Grok** (`.grok-plugin/marketplace.json`).")
out.append("")
out.append("## Plugins")
out.append("")
out.append("| Plugin | Sources | What it does |")
out.append("|--------|---------|--------------|")
# Map descriptions from any catalog
desc_map = {}
for cat in [codex, claude, grok]:
    if not cat: continue
    for p in cat.get("plugins", []):
        desc_map[p["name"]] = p.get("description","")
for p in plugins:
    name = p["name"]
    desc = desc_map.get(name, p.get("description",""))
    srcs = []
    # codex local
    if "path" in p.get("source",{}): srcs.append("Codex: local")
    else: srcs.append("Codex")
    # claude
    if claude and any(x["name"]==name for x in claude.get("plugins",[])): srcs.append("Claude: github/url")
    # grok
    if grok and any(x["name"]==name for x in grok.get("plugins",[])): srcs.append("Grok: url")
    out.append(f"| **{name}** | {', '.join(srcs)} | {desc} |")
out.append("")
out.append("## Install")
out.append("")
out.append("### Codex (local marketplace, recommended)")
out.append("")
out.append("`./plugins/*` are git submodules (not expanded on remote clone), so use the local path:")
out.append("")
out.append("```bash")
out.append("codex plugin marketplace add /Users/fyq/PycharmProjects/agent-plugins")
out.append("codex plugin add devops-ssh@fyq-agent-plugins")
out.append("codex plugin add mcp-ssh-manager@fyq-agent-plugins")
out.append("codex plugin add command-audit@fyq-agent-plugins")
out.append("codex plugin add istoresos@fyq-agent-plugins")
out.append("```")
out.append("")
out.append("`mcp-ssh-manager` needs `npm install --omit=dev` in the Codex cache (`~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/`) — Codex does not auto-install.")
out.append("")
out.append("### Claude Code")
out.append("")
out.append("Claude fetches each plugin from its own repo (github/url + sha), so no submodule init needed. It auto-installs npm deps.")
out.append("")
out.append("```bash")
out.append("claude plugin marketplace add fyq163/agent-plugins")
out.append("claude plugin install devops-ssh@fyq-agent-plugins")
out.append("claude plugin install mcp-ssh-manager@fyq-agent-plugins")
out.append("claude plugin install istoresos@fyq-agent-plugins")
out.append("```")
out.append("")
out.append("### Grok")
out.append("")
out.append("Add `fyq163/agent-plugins` (reads `.grok-plugin/marketplace.json`, `url+sha`). Grok now supports Azure — `devops-ssh` on Azure DevOps is included.")
out.append("")
out.append("```bash")
out.append("grok plugin marketplace add fyq163/agent-plugins  # or via Grok Build UI")
out.append("grok plugin install devops-ssh@fyq-skills --trust")
out.append("grok plugin install mcp-ssh-manager@fyq-skills --trust")
out.append("grok plugin install istoresos@fyq-skills --trust")
out.append("```")
out.append("")
out.append("`path` is omitted for repo-root plugins — fixes `marketplace path is empty`.")
out.append("")
out.append("## Catalogs")
out.append("")
out.append("- Codex: `.agents/plugins/marketplace.json` (local `path`)")
out.append("- Claude Code: `.claude-plugin/marketplace.json` (github/url + sha)")
out.append("- Grok: `.grok-plugin/marketplace.json` (url + sha, no `path` for root)")
out.append("")

pathlib.Path(ROOT / "MARKETPLACE.md").write_text("\n".join(out) + "\n")
print("Wrote MARKETPLACE.md")
