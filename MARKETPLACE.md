# FYQ Agent Plugins — Marketplace

> Auto-generated from marketplace catalogs — do not hand-edit. Edit the catalog JSONs and run `python scripts/generate-marketplace.py`.

This repo is a triple marketplace for **Codex** (`.agents/plugins/marketplace.json`), **Claude Code** (`.claude-plugin/marketplace.json`), and **Grok** (`.grok-plugin/marketplace.json`).

## Plugins

| Plugin | Sources | What it does |
|--------|---------|--------------|
| **command-audit** | Codex: local | Reminds Codex to use apply_patch instead of shell file-writing commands. |
| **devops-ssh** | Codex: local, Claude: github/url, Grok: url | SSH access to personal VPS (osaka1/oracle1/osaka0/oracle0): deploy, healthcheck, logs, file copy, common pitfalls. |
| **mcp-ssh-manager** | Codex, Claude: github/url, Grok: url | SSH remote-server management over MCP for Claude Code / Codex (37 tools: exec, transfer, DB, backups, health monitoring). |
| **istoresos** | Codex, Claude: github/url, Grok: url | Router repair & OpenWrt/iStoreOS operations playbook: network, firewall, wireless troubleshooting, firmware dev (buildroot, ipk, LuCI). |
| **i-have-adhd** | Codex |  |
| **ponytail** | Codex |  |
| **ponytail** | Codex |  |
| **ponytail** | Codex |  |

## Install

### Codex (local marketplace, recommended)

`./plugins/*` are git submodules (not expanded on remote clone), so use the local path:

```bash
codex plugin marketplace add /Users/fyq/PycharmProjects/agent-plugins
codex plugin add devops-ssh@fyq-agent-plugins
codex plugin add mcp-ssh-manager@fyq-agent-plugins
codex plugin add command-audit@fyq-agent-plugins
codex plugin add istoresos@fyq-agent-plugins
```

`mcp-ssh-manager` needs `npm install --omit=dev` in the Codex cache (`~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/`) — Codex does not auto-install.

### Claude Code

Claude fetches each plugin from its own repo (github/url + sha), so no submodule init needed. It auto-installs npm deps.

```bash
claude plugin marketplace add fyq163/agent-plugins
claude plugin install devops-ssh@fyq-agent-plugins
claude plugin install mcp-ssh-manager@fyq-agent-plugins
claude plugin install istoresos@fyq-agent-plugins
```

### Grok

Add `fyq163/agent-plugins` (reads `.grok-plugin/marketplace.json`, `url+sha`). Grok now supports Azure — `devops-ssh` on Azure DevOps is included.

```bash
grok plugin marketplace add fyq163/agent-plugins  # or via Grok Build UI
grok plugin install devops-ssh@fyq-skills --trust
grok plugin install mcp-ssh-manager@fyq-skills --trust
grok plugin install istoresos@fyq-skills --trust
```

`path` is omitted for repo-root plugins — fixes `marketplace path is empty`.

## Catalogs

- Codex: `.agents/plugins/marketplace.json` (local `path`)
- Claude Code: `.claude-plugin/marketplace.json` (github/url + sha)
- Grok: `.grok-plugin/marketplace.json` (url + sha, no `path` for root)

