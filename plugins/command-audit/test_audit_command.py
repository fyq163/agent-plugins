import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from audit_command import writes_file


assert writes_file("cat > tests/example.py <<'EOF'")
assert writes_file("tee -a tests/example.py")
assert writes_file("echo ok > output.txt")
assert not writes_file("cat tests/example.py")
assert not writes_file("echo tee")
# heredoc: only flags when the body actually writes files
assert writes_file("python3 - <<'PY'\nPath('f.py').write_text('x')\nPY")
assert writes_file("python3 - <<'PY'\nopen('f.py', 'w').write('x')\nPY")
assert writes_file("python3 - <<'PY'\nshutil.copy('a', 'b')\nPY")
assert not writes_file("python3 - <<'PY'\nprint('local check only')\nPY")
assert not writes_file("python3 - <<'PY'\nprint('<<EOF write_text trap')\nPY")
assert not writes_file("echo a <<'EOF'\nhello\nEOF")
