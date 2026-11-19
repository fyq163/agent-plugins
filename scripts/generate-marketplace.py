#!/usr/bin/env python3
"""Generate MARKETPLACE.md from the three marketplace catalogs."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_catalog(path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def unique_plugins(entries):
    """Keep the first occurrence of each plugin name, preserving catalog order."""
    result = []
    seen = set()
    for plugin in entries:
        if plugin["name"] not in seen:
            seen.add(plugin["name"])
            result.append(plugin)
    return result


codex = load_catalog(ROOT / ".agents/plugins/marketplace.json")
claude = load_catalog(ROOT / ".claude-plugin/marketplace.json")
grok = load_catalog(ROOT / ".grok-plugin/marketplace.json")

codex_plugins = unique_plugins(codex.get("plugins", []))
claude_plugins = unique_plugins(claude.get("plugins", [])) if claude else []
grok_plugins = unique_plugins(grok.get("plugins", [])) if grok else []
claude_names = {plugin["name"] for plugin in claude_plugins}
grok_names = {plugin["name"] for plugin in grok_plugins}

desc_map = {}
for catalog in (codex, claude, grok):
    if not catalog:
        continue
    for plugin in catalog.get("plugins", []):
        description = plugin.get("description", "")
        if description:
            desc_map.setdefault(plugin["name"], description)

desc_map.setdefault(
    "i-have-adhd",
    "An ADHD-friendly coding-assistant skill focused on action-first, concise answers and clear next steps.",
)
desc_map.setdefault(
    "ponytail",
    "A coding-assistant skill for concise implementation, safer changes, and repository reviews.",
)

install_notes = {
    "command-audit": "The Codex plugin includes its shell-write audit hook; no separate build step is needed.",
    "devops-ssh": "This Codex entry uses a local Azure DevOps submodule. Clone with `--recurse-submodules`, or initialize it with `git -C /path/to/agent-plugins submodule update --init plugins/devops-ssh`. Azure DevOps access is required.",
    "mcp-ssh-manager": "For Codex, install runtime dependencies in the installed plugin cache with `npm install --omit=dev`; Codex does not do this automatically for local or Git plugins. The OpenCode installer below records the Node executable path found at install time.",
    "istoresos": "This skill-focused plugin needs no package build step.",
    "azure-devops-board": "The Azure DevOps skills are bundled in this repository; no package build step is needed.",
    "i-have-adhd": "For client-specific setup, follow the upstream installation guide.",
    "ponytail": "In Codex, open `/hooks`, trust the two lifecycle hooks, and start a new thread after installation.",
}

upstream_guides = {
    "i-have-adhd": "https://github.com/ayghri/i-have-adhd/blob/main/INSTALL.md",
    "ponytail": "https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md",
}

out = [
    "# FYQ Agent Plugins — Marketplace",
    "",
    "> Auto-generated from marketplace catalogs — do not hand-edit. Edit the catalog JSONs and run `python scripts/generate-marketplace.py`.",
    "",
    "This repo is a marketplace for **Codex** (`.agents/plugins/marketplace.json`), **Claude Code** (`.claude-plugin/marketplace.json`), and **Grok** (`.grok-plugin/marketplace.json`).",
    "",
    "## Plugins",
    "",
    "| Plugin | Sources | What it does |",
    "|--------|---------|--------------|",
]

for plugin in codex_plugins:
    name = plugin["name"]
    sources = ["Codex: local" if "path" in plugin.get("source", {}) else "Codex: URL"]
    if name in claude_names:
        sources.append("Claude Code")
    if name in grok_names:
        sources.append("Grok")
    description = desc_map.get(name, "")
    out.append(f"| **{name}** | {', '.join(sources)} | {description} |")

out.extend([
    "",
    "## Install",
    "",
    "Register the marketplace once for the client you use, then install individual plugins from the guide below.",
    "",
    "### Codex",
    "",
    "Clone this repository (use `--recurse-submodules` to include local plugins) and register the checkout:",
    "",
    "```bash",
    "git clone --recurse-submodules https://github.com/fyq163/agent-plugins.git",
    "cd agent-plugins",
    "codex plugin marketplace add \"$PWD\"",
    "```",
    "",
    "### Claude Code",
    "",
    "```bash",
    "claude plugin marketplace add fyq163/agent-plugins",
    "```",
    "",
    "### Grok",
    "",
    "Add the marketplace in Grok Build or run:",
    "",
    "```bash",
    "grok plugin marketplace add fyq163/agent-plugins",
    "```",
    "",
    "## Install by plugin",
    "",
])

for plugin in codex_plugins:
    name = plugin["name"]
    description = desc_map.get(name, "")
    out.extend([f"### `{name}`", ""])
    if description:
        out.extend([description, ""])
    out.append(f"- **Codex:** `codex plugin add {name}@{codex['name']}`")
    if name in claude_names and claude:
        out.append(f"- **Claude Code:** `claude plugin install {name}@{claude['name']}`")
    if name in grok_names and grok:
        out.append(f"- **Grok:** `grok plugin install {name}@{grok['name']} --trust`")
    note = install_notes.get(name)
    if note:
        out.append(f"- **Setup:** {note}")
    if name in upstream_guides:
        out.append(f"- **Upstream guide:** {upstream_guides[name]}")
    if name == "mcp-ssh-manager":
        out.append("- **OpenCode:** `curl -fsSL https://raw.githubusercontent.com/fyq163/mcp-ssh-manager-as-plugins/codex-oc-plugins/scripts/install-opencode.sh | bash`")
    out.append("")

out.extend([
    "## Catalogs",
    "",
    "- Codex: `.agents/plugins/marketplace.json`",
    "- Claude Code: `.claude-plugin/marketplace.json`",
    "- Grok: `.grok-plugin/marketplace.json`",
    "",
])

(ROOT / "MARKETPLACE.md").write_text("\n".join(out))
print("Wrote MARKETPLACE.md")
