from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[3]
DB_ROOT = os.path.join(ROOT, 'data', 'chroma_db')
print(DB_ROOT)
