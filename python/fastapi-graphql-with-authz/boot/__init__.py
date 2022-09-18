import sys
from pathlib import Path

__all__ = ["BASE_DIR"]

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR.as_posix())
