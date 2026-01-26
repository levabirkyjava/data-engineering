import os
import click
import pandas as pd
from sqlalchemy import create_engine

def _engine(user, password, host, port, db):
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def _load_green_parquet(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    for c in ["lpep_pickup_datetime", "lpep_dropoff_datetime"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
    return df

def _load_zones_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@click.command()
@click.option("--pg-user", default="root")
@click.option("--pg-pass", default="root")
@click.option("--pg-host", default="localhost")
@click.option("--pg-port", default=5432, type=int)
@click.option("--pg-db", default="ny_taxi")
@click.option("--green-path", required=True, help="Path to green_tripdata_2025-11.parquet")
@click.option("--zones-path", required=True, help="Path to taxi_zone_lookup.csv")
@click.option("--green-table", default="green_tripdata")
@click.option("--zones-table", default="zones")
@click.option("--chunksize", default=100_000, type=int)
def main(pg_user, pg_pass, pg_host, pg_port, pg_db,
         green_path, zones_path, green_table, zones_table, chunksize):

    engine = _engine(pg_user, pg_pass, pg_host, pg_port, pg_db)

    zones = _load_zones_csv(zones_path)
    zones.to_sql(zones_table, engine, if_exists="replace", index=False)

    df = _load_green_parquet(green_path)

    df.head(0).to_sql(green_table, engine, if_exists="replace", index=False)

    df.to_sql(green_table, engine, if_exists="append", index=False, chunksize=chunksize, method="multi")

if __name__ == "__main__":
    main()
