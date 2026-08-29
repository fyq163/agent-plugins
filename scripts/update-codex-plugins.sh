#!/usr/bin/env bash
# update-codex-plugins.sh — quickly update plugin(s) from the local marketplace
# by remove + re-add (Codex has no `plugin update` command).
#
# Usage:
#   scripts/update-codex-plugins.sh                   # update ALL plugins in the Codex catalog
#   scripts/update-codex-plugins.sh mcp-ssh-manager   # update specific plugin(s), repeatable
#
# Notes:
# - Only refreshes what the marketplace snapshot serves. For git-based
#   marketplaces run `codex plugin marketplace upgrade` first; the local
#   fyq-agent-plugins snapshot is this repo dir itself, so pull/rebase first.
# - (Re)install resets the plugin cache — re-apply the README cache patches
#   afterwards if your Codex version needs them (PLUGIN_ROOT on 0.149.1,
#   SessionEnd timeout 3s).

set -u

MARKETPLACE="fyq-agent-plugins"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ $# -gt 0 ]; then
  plugins=("$@")
else
  # all plugin names from the Codex catalog (names are simple identifiers,
  # so word-splitting is safe)
  plugins=$(python3 -c \
    "import json;print('\n'.join(p['name'] for p in json.load(open('.agents/plugins/marketplace.json'))['plugins']))")
fi

fail=0
for p in $plugins; do
  echo "== $p =="
  codex plugin remove "$p@$MARKETPLACE" >/dev/null 2>&1 || echo "   (not installed, skipping remove)"
  if codex plugin add "$p@$MARKETPLACE"; then
    echo "   ok"
  else
    echo "   FAILED" >&2
    fail=1
  fi
done

if [ "$fail" -eq 0 ]; then
  echo "all done"
else
  echo "some plugins failed, see output above" >&2
fi
exit "$fail"
