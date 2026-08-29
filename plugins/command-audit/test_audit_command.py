import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from audit_command import writes_file


assert writes_file("cat > tests/example.py <<'EOF'")
assert writes_file("tee -a tests/example.py")
assert writes_file("echo ok > output.txt")
assert not writes_file("cat tests/example.py")
assert not writes_file("echo tee")
