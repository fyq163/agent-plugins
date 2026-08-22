# FYQ Agent Plugins — Marketplace

This repo is a dual plugin marketplace for **OpenAI Codex** and **Grok Build**.
It bundles personal skills and MCP servers as installable plugins.

- Codex catalog: `.agents/plugins/marketplace.json` (local source → `./plugins/<name>`)
- Grok catalog: `.grok-plugin/marketplace.json` (each plugin fetched from its own repo, pinned to a `sha`)

## Plugins

| Plugin | Type | What it does |
|--------|------|--------------|
| **devops-ssh** | skill | SSH access to personal VPS (osaka1/oracle1/osaka0/oracle0): deploy, healthcheck, logs, file copy, common pitfalls. |
| **mcp-ssh-manager** | MCP server | SSH remote-server management over MCP for Claude Code / Codex (37 tools: exec, transfer, DB, backups, health monitoring). Needs Node.js deps installed (see below). |
| **istoresos** | skill | Router repair & OpenWrt/iStoreOS operations playbook: network, firewall, wireless troubleshooting, firmware dev (buildroot, ipk, LuCI). |

## Install on Codex

Use the **local** marketplace (recommended). Plugins live in `plugins/` as git
submodules, which are NOT expanded when Codex clones a marketplace from a remote
URL — so a Git-marketplace install would fetch empty plugin dirs. The local path
avoids that.

```bash
# from the repo root, or use the absolute path
codex plugin marketplace add /Users/fyq/PycharmProjects/agent-plugins

codex plugin add devops-ssh@fyq-agent-plugins
codex plugin add mcp-ssh-manager@fyq-agent-plugins
codex plugin add istoresos@fyq-agent-plugins
```

### mcp-ssh-manager needs its deps installed manually

Codex does **not** auto-run `npm install` for local/git plugins. After installing,
install the runtime deps once in the installed cache dir, or the MCP server
crashes on startup (`connection closed: initialize response`):

```bash
cd ~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/3.8.0
npm install --omit=dev
```

### Refreshing after a submodule update

`codex plugin marketplace upgrade` only works for **Git** marketplaces; this is a
local one, so it does nothing here. To pick up a plugin code change after you
update its submodule, re-install the plugin:

```bash
codex plugin remove mcp-ssh-manager@fyq-agent-plugins
codex plugin add mcp-ssh-manager@fyq-agent-plugins
# then re-run the npm install step above
```

## Install on Grok

Grok reads `.grok-plugin/marketplace.json`. Add this repo as a marketplace in
Grok Build (point it at the GitHub repo `fyq163/agent-plugins`); Grok fetches
each plugin from the `url` + `sha` + `path` listed in that catalog, so each
plugin is pinned to a specific commit of its own source repo.

```bash
# conceptual — done in the Grok Build UI by adding the marketplace URL
# then install individual plugins from the directory
```

Notes:
- `mcp-ssh-manager` and `istoresos` are on GitHub and fetch fine.
- `devops-ssh` lives in **Azure DevOps** (`sebfan/oracle-devops/_git/devops-ssh-skill`).
  Grok may not be able to fetch it (GitHub-only), so it may not appear / install.
- Like on Codex, `mcp-ssh-manager` needs its Node.js deps; install them in the
  Grok plugin cache after install.

## How it's structured

```
.agents/plugins/marketplace.json     # Codex catalog (local sources)
.grok-plugin/marketplace.json        # Grok catalog (url + sha + path)
plugins/
  devops-ssh/                       # git submodule (Azure DevOps)
  codex-plugin-ssh-manager/         # git submodule (GitHub, feat branch)
    .codex-plugin/plugin.json
    .mcp.json                       # launches node src/index.js
    src/index.js
  istoresos/                        # git submodule (GitHub)
```

The `plugins/` tree is made of git submodules. To update a plugin, work inside
its submodule, push there, then update the parent pointer (and the Grok `sha`)
in this repo.
