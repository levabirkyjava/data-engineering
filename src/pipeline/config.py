from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime settings loaded from environment variables."""

    project_id: str
    raw_dataset: str = "raw"
    analytics_dataset: str = "analytics"
    source_table: str = "bigquery-public-data.chicago_taxi_trips.taxi_trips"

    @classmethod
    def from_env(cls) -> "PipelineConfig":
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID is required")

        return cls(
            project_id=project_id,
            raw_dataset=os.getenv("RAW_DATASET", "raw"),
            analytics_dataset=os.getenv("ANALYTICS_DATASET", "analytics"),
            source_table=os.getenv(
                "SOURCE_TABLE",
                "bigquery-public-data.chicago_taxi_trips.taxi_trips",
            ),
        )

