# Skills Marketplace

This repo doubles as an [OpenAI Codex / ChatGPT plugin marketplace](https://developers.openai.com/plugins).
It bundles my personal skills, scripts, and MCP servers into installable plugins so I can
browse and install them from any machine.

## What's inside (discovery)

| Plugin | Type | Version | What it does |
|--------|------|---------|--------------|
| **devop-ssh** | skill | 1.0.0 | SSH access to personal VPS (osaka1/oracle1/osaka0/oracle0): deploy, healthcheck, logs, file copy, common pitfalls. |
| **r2-sync** | skill + script | 1.0.0 | Bidirectional file sync between a local dir and Cloudflare R2 (three-way merge, conflict resolution). Replaces Obsidian sync. |
| **mcp-ssh-manager** | MCP server | 3.8.0 | SSH remote-server management over MCP for Claude Code / Codex (commands, file transfer, DB, backups, health). |
| **istoresos** | skill | 1.0.0 | Router repair and OpenWrt/iStoreOS operations playbook: DNS/DHCP/firewall/WAN/LAN/wireless troubleshooting, firmware dev (buildroot, ipk, LuCI), router config. |

## Install from GitHub (one command)

### 1. Add the marketplace

```bash
# clone-on-demand from GitHub (Codex fetches it for you)
# NOTE: marketplace lives on the `plug-in` branch (main has no marketplace files)
codex plugin marketplace add fyq163/windows_automation --ref plug-in

# optional: only fetch the marketplace + plugin files (skips the rest of the repo)
codex plugin marketplace add fyq163/windows_automation --ref plug-in --sparse .agents/plugins --sparse plugins
```

To pin a branch/ref (the marketplace lives on `plug-in`, not `main`):

```bash
codex plugin marketplace add fyq163/windows_automation --ref plug-in
```

### 2. Install a plugin

```bash
codex plugin add devop-ssh
codex plugin add r2-sync
codex plugin add mcp-ssh-manager
codex plugin add istoresos
```

Or list everything available first:

```bash
codex plugin list
```

### 3. In the ChatGPT / Codex desktop app

1. Open the **Plugins Directory**.
2. Choose **Add marketplace** → point it at `fyq163/windows_automation`.
3. Browse the curated list and install with one click.

## Manage marketplaces

```bash
codex plugin marketplace list          # see configured sources
codex plugin marketplace upgrade        # refresh snapshots
codex plugin marketplace remove fyq163/windows_automation
```

## Local testing (before pushing)

```bash
# from the repo root
codex plugin marketplace add .
codex plugin list
# when done:
codex plugin marketplace remove fyq-skills
```

## How it's structured

```
.agents/plugins/marketplace.json     # the catalog (points at ./plugins/<name>)
plugins/
  devop-ssh/
    .codex-plugin/plugin.json        # manifest
    skills/devop-ssh/SKILL.md        # self-contained copy
  r2-sync/
    .codex-plugin/plugin.json
    skills/r2-sync/SKILL.md
    skills/r2-sync/sync.py           # engine (copied in, self-contained)
    skills/r2-sync/requirements.txt
  mcp-ssh-manager/
    .codex-plugin/plugin.json
    .mcp.json                        # bundled MCP server (pulled via npx)
  istoresos/
    .codex-plugin/plugin.json
    skills/istoresos/               # full skill copy (SKILL.md + prompts/references/templates/tools)
```

The `plugins/` tree is **self-contained** — it does not depend on the `skills/`
git submodules, so a fresh `git clone` + `codex plugin marketplace add` works
without recursive submodule init.

## Add a new plugin

1. Create `plugins/<name>/.codex-plugin/plugin.json` (see existing ones).
2. Add `skills/`, `.mcp.json`, or `hooks/` as needed (all paths relative to the
   plugin root, start with `./`).
3. Register it in `.agents/plugins/marketplace.json` under `plugins[]` with
   `source.path: "./plugins/<name>"`.
4. Commit and push; everyone gets it on next `codex plugin marketplace upgrade`.
