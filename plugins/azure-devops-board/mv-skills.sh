#!/usr/bin/env bash
# Sync the curated Azure DevOps skills from upstream Agent-Skills into this plugin.
#
# Usage: ./mv-skills.sh [skill ...]
#   no args -> azure-boards azure-devops azure-pipelines
#
# Upstream checkout defaults to ../tools/Agent-Skills relative to the marketplace
# repo root; override with AGENT_SKILLS_DIR=/path/to/Agent-Skills.
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$PLUGIN_DIR/skills"
REPO_ROOT="$(cd "$PLUGIN_DIR/../.." && pwd)"
UPSTREAM="${AGENT_SKILLS_DIR:-$(cd "$REPO_ROOT/.." && pwd)/tools/Agent-Skills}"

SKILLS=(azure-boards azure-devops azure-pipelines)
if [ "$#" -gt 0 ]; then
	SKILLS=("$@")
fi

if [ ! -d "$UPSTREAM/.git" ]; then
	echo "upstream Agent-Skills checkout not found: $UPSTREAM" >&2
	echo "set AGENT_SKILLS_DIR=/path/to/Agent-Skills and re-run" >&2
	exit 1
fi

echo "==> syncing $UPSTREAM"
git -C "$UPSTREAM" pull --ff-only

mkdir -p "$SKILLS_DIR"
for skill in "${SKILLS[@]}"; do
	src="$UPSTREAM/skills/$skill"
	if [ ! -d "$src" ]; then
		# restore files removed by older `mv`-based runs
		git -C "$UPSTREAM" checkout -- "skills/$skill"
	fi
	if [ ! -d "$src" ]; then
		echo "    skip (not in upstream): $skill" >&2
		continue
	fi
	rm -rf "$SKILLS_DIR/$skill"
	cp -R "$src" "$SKILLS_DIR/$skill"
	echo "    copied $skill"
done

echo "==> done: $SKILLS_DIR"
