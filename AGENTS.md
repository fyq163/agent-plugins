# AGENTS.md — agent-plugins (Codex + Grok plugin marketplace)

This repo is a **plugin marketplace** that bundles personal plugins (skills + MCP
servers) for two clients: **Codex** (`.agents/plugins/marketplace.json`) and
**Grok** (`.grok-plugin/marketplace.json`). Plugins live in `plugins/<name>/` as
**git submodules**.

## Layout

```
agent-plugins/
├── .agents/plugins/marketplace.json   # Codex catalog (local source → ./plugins/<name>)
├── .grok-plugin/marketplace.json      # Grok catalog (url + sha + path per plugin)
└── plugins/
    ├── codex-plugin-ssh-manager/      # GitHub: fyq163/mcp-ssh-manager-as-plugins @ feat/ssh-manager-codex-plugin
    ├── devops-ssh/                    # Azure DevOps: devops-ssh-skill (NOT GitHub)
    └── istoresos/                     # GitHub: fyq163/router-repair
```

## Update method (read this before touching anything)

**Our marketplace files are at the repo ROOT, not inside any submodule.** They are
edited directly in the parent repo and committed to `main`. Submodule updates
never touch them.

**You do NOT need `git checkout main -- <file>` tricks.** That pattern is for
pulling specific files out of a branch; it is not how this repo is maintained.
The only files that matter at the root are the two `marketplace.json` catalogs —
edit them in place.

### Updating a plugin's code
1. `cd plugins/<name>` and work on the correct branch (see below).
2. Commit + push **inside the submodule**.
3. In the parent: `git add plugins/<name>` (updates the gitlink pointer) and commit.
4. If the plugin is listed in `.grok-plugin/marketplace.json`, bump its `sha` to
   the new submodule HEAD and commit that too.

### Upstream cruft (the marketplace.json problem)
Each submodule is a full upstream repo and carries its own junk, e.g.
`plugins/codex-plugin-ssh-manager/.agents/plugins/marketplace.json` (an inner
marketplace that points at a deleted nested dir) and a README that calls the
plugin `mcp-ssh-manager-plugin`. This inner marketplace is **inert** — Codex only
reads the root `.agents/plugins/marketplace.json`. We cleaned it in the
submodule's own branch (deleted the inner file, fixed README/.gitignore).

**Risk:** a blind `git submodule update --remote` re-fetches upstream's latest and
can re-introduce that cruft. Mitigation: track our own branch (`feat/...`) and
avoid `--remote` pulls; clean cruft in the submodule branch, not via checkout
hacks. The root marketplace is unaffected either way.

## Submodule specifics

| Plugin | Remote | Branch / notes |
|--------|--------|----------------|
| `codex-plugin-ssh-manager` | GitHub `fyq163/mcp-ssh-manager-as-plugins` | developed on `feat/ssh-manager-codex-plugin` (NOT `main`) |
| `devops-ssh` | Azure `git@ssh.dev.azure.com:v3/sebfan/oracle-devops/devops-ssh-skill` | `gh` CANNOT touch Azure — use Azure CLI/web |
| `istoresos` | GitHub `fyq163/router-repair` | — |

- `devop-ssh` was renamed to `devops-ssh` locally; the Azure repo is still
  `devops-ssh-skill`. Keep the local name consistent in both catalogs.
- `mcp-ssh-manager` plugin manifest name is `mcp-ssh-manager` (the upstream
  README's `mcp-ssh-manager-plugin` is wrong — don't propagate it).

## Grok catalog gotcha
Grok cannot fetch from a local path and submodules are NOT expanded on fetch, so
each entry uses `source: "url"` + `path: "./"` pointing at the plugin's **own**
repo root, pinned to a `sha`. Do not point Grok at the monorepo subdir — the
fetched dir would be empty. `devops-ssh` lives in Azure; Grok may not fetch it.

## Push gotchas
Submodule remotes may be HTTPS and return 403 on push. Switch to SSH first:
`git -C plugins/<name> remote set-url origin git@github.com:fyq163/<repo>.git`.
The parent repo pushes fine over SSH.

## Local install (for testing)
```
codex plugin marketplace add /Users/fyq/PycharmProjects/agent-plugins
codex plugin add <name>@fyq-agent-plugins
```
Codex does NOT auto-run `npm install` for local/git plugins. `mcp-ssh-manager`'s
`.mcp.json` launches `node src/index.js` directly; you must `npm install --omit=dev`
in the installed cache dir (`~/.codex/plugins/cache/fyq-agent-plugins/mcp-ssh-manager/<version>/`)
or the MCP server crashes on startup (`connection closed: initialize response`).
