import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// Detection rules live in ../audit_command.py (shared with the Codex hook).
// This extension only adapts them to pi's event API.
const here =
	typeof __dirname === "string" ? __dirname : path.dirname(fileURLToPath(import.meta.url));
const AUDIT_SCRIPT = path.resolve(here, "..", "audit_command.py");

const REMINDER =
	"[command-audit] Prefer the `edit`/`write` tools for modifying files instead of " +
	"shell redirection (`>`/`>>`), `tee`, or `cat <<EOF` writing to a file.";

function writesFile(command: string): boolean {
	try {
		// Same stdin contract as the Codex PreToolUse hook.
		const result = spawnSync("python3", [AUDIT_SCRIPT], {
			input: JSON.stringify({ tool_name: "Bash", tool_input: { command } }),
			encoding: "utf-8",
			timeout: 5000,
		});
		if (result.error || result.status !== 0 || !result.stdout) return false;
		return Boolean(JSON.parse(result.stdout)?.hookSpecificOutput);
	} catch {
		return false;
	}
}

export default function (pi: ExtensionAPI) {
	pi.on("tool_result", async (event) => {
		if (event.toolName !== "bash") return;
		const command = event.input?.command;
		if (typeof command !== "string" || command === "") return;
		if (!writesFile(command)) return;

		return {
			content: [...event.content, { type: "text" as const, text: REMINDER }],
		};
	});
}
