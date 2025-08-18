import os
import sys
from pathlib import Path

os.environ.setdefault("JWT_SECRET", "s" * 32)

sys.path.append(str(Path(__file__).resolve().parents[1]))
