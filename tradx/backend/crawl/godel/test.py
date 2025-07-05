import tradx
from pathlib import Path

root_path = Path(tradx.__file__).resolve().parent
print(root_path)