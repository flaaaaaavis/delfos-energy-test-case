from sqlalchemy import create_engine

def get_engine(conn_string: str):
    return create_engine(conn_string)

def load(df, engine):
    df.to_sql("data", engine, if_exists="append", index=False)