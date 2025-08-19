import os
import sys
from pathlib import Path

os.environ.setdefault("JWT_SECRET", "s" * 32)
os.environ.setdefault("SUPABASE_URL", "http://test")
os.environ.setdefault("SUPABASE_KEY", "test")

sys.path.append(str(Path(__file__).resolve().parents[1]))
