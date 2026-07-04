from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = Path(os.getenv('DATA_ROOT', ROOT / 'data'))
RAW = DATA_ROOT / 'raw'
REFERENCE = DATA_ROOT / 'reference'
DOCUMENTS = DATA_ROOT / 'documents'
BRONZE = DATA_ROOT / 'bronze'
SILVER = DATA_ROOT / 'silver'
GOLD = DATA_ROOT / 'gold'
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'openai/gpt-oss-20b:free')
for p in [RAW, REFERENCE, DOCUMENTS, BRONZE, SILVER, GOLD]:
    p.mkdir(parents=True, exist_ok=True)
