from .extract import extract
from .transform import transform
from .load import load, get_engine
from .config import API_URL, DB_TARGET

def run_etl(date: str):
    raw = extract(date, API_URL)
    df = transform(raw)

    engine = get_engine(DB_TARGET)
    load(df, engine)

if __name__ == "__main__":
    import sys
    run_etl(sys.argv[1])
