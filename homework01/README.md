# data-engineering
Learn data-engineering



What’s inside

    homework01/docker-compose.yaml — Postgres + pgAdmin

    homework01/ingest.py — loads NYC TLC Green Taxi (2025-11) and zones into Postgres

    homework01/green_tripdata_2025-11.parquet

    homework01/taxi_zone_lookup.csv

Prerequisites

    Docker + Docker Compose

    Python (project venv) + dependencies from homework01/pyproject.toml

Run Postgres + pgAdmin

From homework01/:

bash
docker compose up -d

pgAdmin:

    URL: http://localhost:8085

    Email: admin@admin.com

    Password: root

Postgres (from host):

    host: localhost

    port: 5432

    db: ny_taxi

    user/pass: root / root

Load data into Postgres

Run ingestion from homework01/:

bash
python ingest.py \
  --pg-host localhost --pg-port 5432 --pg-db ny_taxi --pg-user root --pg-pass root \
  --green-path ./green_tripdata_2025-11.parquet \
  --zones-path ./taxi_zone_lookup.csv

Tables created:

    green_tripdata

    zones
