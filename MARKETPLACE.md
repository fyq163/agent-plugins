# FYQ Agent Plugins — Marketplace

> Auto-generated from marketplace catalogs — do not hand-edit. Edit the catalog JSONs and run `python scripts/generate-marketplace.py`.

This repo is a marketplace for **Codex** (`.agents/plugins/marketplace.json`), **Claude Code** (`.claude-plugin/marketplace.json`), and **Grok** (`.grok-plugin/marketplace.json`).

## Plugins

| Plugin | Sources | What it does |
|--------|---------|--------------|
| **command-audit** | Codex: local | Reminds Codex to use apply_patch instead of shell file-writing commands. |
| **devops-ssh** | Codex: local, Claude Code, Grok | SSH access to personal VPS (osaka1/oracle1/osaka0/oracle0): deploy, healthcheck, logs, file copy, common pitfalls. |
| **mcp-ssh-manager** | Codex: URL, Claude Code, Grok | SSH remote-server management over MCP for Claude Code / Codex (37 tools: exec, transfer, DB, backups, health monitoring). |
| **istoresos** | Codex: URL, Claude Code, Grok | Router repair & OpenWrt/iStoreOS operations playbook: network, firewall, wireless troubleshooting, firmware dev (buildroot, ipk, LuCI). |
| **i-have-adhd** | Codex: URL | An ADHD-friendly coding-assistant skill focused on action-first, concise answers and clear next steps. |
| **ponytail** | Codex: URL | A coding-assistant skill for concise implementation, safer changes, and repository reviews. |
| **azure-devops-board** | Codex: local | Curated Azure DevOps skills synced from MicrosoftDocs/Agent-Skills: work items & queries (azure-boards), orgs/agent pools/Analytics (azure-devops), YAML pipelines & service connections (azure-pipelines). |

## Install

Register the marketplace once for the client you use, then install individual plugins from the guide below.

### Codex

Clone this repository (use `--recurse-submodules` to include local plugins) and register the checkout:

```bash
git clone --recurse-submodules https://github.com/fyq163/agent-plugins.git
cd agent-plugins
codex plugin marketplace add "$PWD"
```

### Claude Code

```bash
claude plugin marketplace add fyq163/agent-plugins
```

### Grok

Add the marketplace in Grok Build or run:

```bash
grok plugin marketplace add fyq163/agent-plugins
```

## Install by plugin

### `command-audit`

Reminds Codex to use apply_patch instead of shell file-writing commands.

- **Codex:** `codex plugin add command-audit@fyq-agent-plugins`
- **Setup:** The Codex plugin includes its shell-write audit hook; no separate build step is needed.

### `devops-ssh`

SSH access to personal VPS (osaka1/oracle1/osaka0/oracle0): deploy, healthcheck, logs, file copy, common pitfalls.

- **Codex:** `codex plugin add devops-ssh@fyq-agent-plugins`
- **Claude Code:** `claude plugin install devops-ssh@fyq-agent-plugins`
- **Grok:** `grok plugin install devops-ssh@fyq-skills --trust`
- **Setup:** This Codex entry uses a local Azure DevOps submodule. Clone with `--recurse-submodules`, or initialize it with `git -C /path/to/agent-plugins submodule update --init plugins/devops-ssh`. Azure DevOps access is required.

### `mcp-ssh-manager`

SSH remote-server management over MCP for Claude Code / Codex (37 tools: exec, transfer, DB, backups, health monitoring).

- **Codex:** `codex plugin add mcp-ssh-manager@fyq-agent-plugins`
- **Claude Code:** `claude plugin install mcp-ssh-manager@fyq-agent-plugins`
- **Grok:** `grok plugin install mcp-ssh-manager@fyq-skills --trust`
- **Setup:** For Codex, install runtime dependencies in the installed plugin cache with `npm install --omit=dev`; Codex does not do this automatically for local or Git plugins. The OpenCode installer below records the Node executable path found at install time.
- **OpenCode:** `curl -fsSL https://raw.githubusercontent.com/fyq163/mcp-ssh-manager-as-plugins/codex-oc-plugins/scripts/install-opencode.sh | bash`

### `istoresos`

Router repair & OpenWrt/iStoreOS operations playbook: network, firewall, wireless troubleshooting, firmware dev (buildroot, ipk, LuCI).

- **Codex:** `codex plugin add istoresos@fyq-agent-plugins`
- **Claude Code:** `claude plugin install istoresos@fyq-agent-plugins`
- **Grok:** `grok plugin install istoresos@fyq-skills --trust`
- **Setup:** This skill-focused plugin needs no package build step.

### `i-have-adhd`

An ADHD-friendly coding-assistant skill focused on action-first, concise answers and clear next steps.

- **Codex:** `codex plugin add i-have-adhd@fyq-agent-plugins`
- **Setup:** For client-specific setup, follow the upstream installation guide.
- **Upstream guide:** https://github.com/ayghri/i-have-adhd/blob/main/INSTALL.md

### `ponytail`

A coding-assistant skill for concise implementation, safer changes, and repository reviews.

- **Codex:** `codex plugin add ponytail@fyq-agent-plugins`
- **Setup:** In Codex, open `/hooks`, trust the two lifecycle hooks, and start a new thread after installation.
- **Upstream guide:** https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md

### `azure-devops-board`

Curated Azure DevOps skills synced from MicrosoftDocs/Agent-Skills: work items & queries (azure-boards), orgs/agent pools/Analytics (azure-devops), YAML pipelines & service connections (azure-pipelines).

- **Codex:** `codex plugin add azure-devops-board@fyq-agent-plugins`
- **Setup:** The Azure DevOps skills are bundled in this repository; no package build step is needed.

## Catalogs

- Codex: `.agents/plugins/marketplace.json`
- Claude Code: `.claude-plugin/marketplace.json`
- Grok: `.grok-plugin/marketplace.json`
