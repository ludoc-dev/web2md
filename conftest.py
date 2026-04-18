import sys
from pathlib import Path

# Add the parent directory of 'auto_prompt' to sys.path
# This makes 'auto_prompt' importable as a top-level package
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))