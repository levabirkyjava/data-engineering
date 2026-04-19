from __future__ import annotations

from datetime import date

from pipeline.config import PipelineConfig
from pipeline.sql import (
    build_create_raw_table_sql,
    build_incremental_insert_sql,
    build_tile_queries,
)


def main() -> None:
    cfg = PipelineConfig.from_env()

    print("-- CREATE RAW TABLE --")
    print(build_create_raw_table_sql(cfg))
    print()

    print("-- INCREMENTAL INSERT (example date) --")
    print(build_incremental_insert_sql(cfg, date(2024, 1, 1)))
    print()

    print("-- TILE QUERIES --")
    for name, sql in build_tile_queries(cfg).items():
        print(f"[{name}]")
        print(sql)
        print()


if __name__ == "__main__":
    main()

