# agent-plugins

> **My personal setup.** This is not an official marketplace — it's just a bundle of
> Codex plugins I use (plus a few others), collected here for my own machines.

## What's in here

This repo is a Codex plugin marketplace that bundles the plugins I actually use,
along with some extra plugins. Each plugin lives in `plugins/<name>/` as a git
submodule.

```
agent-plugins/
├── .agents/plugins/marketplace.json   # Codex catalog
├── .grok-plugin/marketplace.json      # Grok catalog (if you also use Grok)
└── plugins/                           # actual plugin code (submodules)
    ├── codex-plugin-ssh-manager/
    ├── devops-ssh/
    └── istoresos/
```

## Install locally

```bash
codex plugin marketplace add /Users/fyq/sources/agent-plugins
codex plugin add <name>@fyq-agent-plugins
```

## Backup MCP servers

These are the MCP servers I keep configured. Re-add them when rebuilding a machine.

### github-cli (gh-mcp)

```bash
codex mcp add github-cli gh mcp
```

Source: https://github.com/shuymn/gh-mcp

### context7

Add to your Codex config (`~/.codex/config.toml`):

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"

[mcp_servers.context7.http_headers]
CONTEXT7_API_KEY = "<your-context7-api-key>"
```

## Plugin MCP: `${PLUGIN_ROOT}` gotcha

Plugins that ship an MCP server (e.g. `codex-plugin-ssh-manager`) declare it in
their `.mcp.json` with a placeholder path:

```json
{ "mcpServers": { "mcp-ssh-manager": { "command": "node", "args": ["${PLUGIN_ROOT}/src/index.js"] } } }
```

When Codex launches the plugin's MCP server, it **in practice** expands
`${PLUGIN_ROOT}` to the plugin's install dir under
`~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`. This is **de-facto
supported behavior in current Codex**, NOT a written contract: the official build
docs only document `PLUGIN_ROOT` (and the compat `CLAUDE_PLUGIN_ROOT`) as an
*environment variable passed to plugin hook commands*, and never show variable
substitution inside `.mcp.json` args. Treat the placeholder as "works on recent
Codex", not "guaranteed by spec".

### Why this matters (0.149.1 bug)

Codex **0.149.1** does not expand `${PLUGIN_ROOT}` in `.mcp.json` args — it joins
the literal string onto the marketplace dir, which crashes the server on startup
(`MODULE_NOT_FOUND` → `connection closed: initialize response`). After any
install/upgrade on a buggy version, patch the cached copy to an absolute path:

```bash
# find it
ls ~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/.mcp.json
# change
"args": ["${PLUGIN_ROOT}/src/index.js"]
# to
"args": ["/Users/fyq/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/src/index.js"]
```

Keep the submodule source as-is (with `${PLUGIN_ROOT}`) — that's the correct
syntax for newer Codex. Only the local buggy client needs the cached copy patched.

### Also: deps aren't installed automatically

Codex does **not** run `npm install` for local/git plugins. If the MCP server
won't start even with the right path, install deps in the cache dir:

```bash
cd ~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/
npm install --omit=dev
```
