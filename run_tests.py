import subprocess, sys
result = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    text=True
)
raise SystemExit(result.returncode)
