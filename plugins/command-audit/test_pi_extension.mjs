import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
import path from "node:path";

const ext = await import(
	pathToFileURL(path.join(import.meta.dirname, "extensions", "command-audit.ts")).href
);

function loadExtension() {
	const handlers = {};
	const pi = {
		on: (name, handler) => {
			handlers[name] = handler;
		},
	};
	ext.default(pi);
	assert.ok(handlers.tool_result, "tool_result handler registered");
	return handlers.tool_result;
}

async function run(handler, command) {
	return handler(
		{ toolName: "bash", toolCallId: "t1", input: { command }, content: [{ type: "text", text: "ok" }] },
		{},
	);
}

const onToolResult = loadExtension();

for (const command of [
	"echo ok > output.txt",
	"tee -a tests/example.py",
	"cat > f.py <<'EOF'",
	"python3 - <<'PY'\nPath('f.py').write_text('x')\nPY",
]) {
	const patch = await run(onToolResult, command);
	assert.ok(patch?.content?.at(-1)?.text.includes("command-audit"), `flagged: ${command}`);
}

for (const command of ["cat tests/example.py", "echo tee", "grep -r foo src | head"]) {
	assert.equal(await run(onToolResult, command), undefined, `not flagged: ${command}`);
}

// other tools are untouched
assert.equal(
	await onToolResult(
		{ toolName: "write", toolCallId: "t2", input: { path: "f.py" }, content: [] },
		{},
	),
	undefined,
);

console.log("pi extension tests passed");
