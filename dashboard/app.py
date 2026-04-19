from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
from google.cloud import bigquery

from pipeline.config import PipelineConfig


@st.cache_resource
def get_client(project_id: str) -> bigquery.Client:
    return bigquery.Client(project=project_id)


@st.cache_data(ttl=3600)
def load_temporal_data(project_id: str, analytics_dataset: str) -> pd.DataFrame:
    client = get_client(project_id)
    query = f"""
    SELECT
      trip_date,
      trips_cnt
    FROM `{project_id}.{analytics_dataset}.mart_trips_daily`
    ORDER BY trip_date
    """
    return normalize_trip_date_column(client.query(query).to_dataframe())


@st.cache_data(ttl=3600)
def load_payment_data(project_id: str, analytics_dataset: str) -> pd.DataFrame:
    client = get_client(project_id)
    query = f"""
    SELECT
      trip_date,
      payment_type,
      trips_cnt
    FROM `{project_id}.{analytics_dataset}.mart_payment_type_daily`
    """
    return normalize_trip_date_column(client.query(query).to_dataframe())


def normalize_trip_date_column(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized["trip_date"] = pd.to_datetime(normalized["trip_date"], errors="coerce").dt.date
    return normalized.dropna(subset=["trip_date"])


def apply_date_filter(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    if df.empty:
        return df
    return df[(df["trip_date"] >= start_date) & (df["trip_date"] <= end_date)].copy()


def main() -> None:
    st.set_page_config(page_title="Chicago Taxi Dashboard", layout="wide")
    st.title("Chicago Taxi Trips Dashboard")
    st.caption("Source: BigQuery marts built by dbt")

    cfg = PipelineConfig.from_env()

    temporal_df = load_temporal_data(cfg.project_id, cfg.analytics_dataset)
    payment_df = load_payment_data(cfg.project_id, cfg.analytics_dataset)

    if temporal_df.empty or payment_df.empty:
        st.warning(
            "No data found in analytics marts. Run the DAG and dbt models before opening the dashboard."
        )
        return

    min_date = temporal_df["trip_date"].min()
    max_date = temporal_df["trip_date"].max()

    col1, col2 = st.columns([2, 1])
    with col1:
        date_range = st.date_input(
            "Trip date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    with col2:
        st.metric("Available period", f"{min_date} to {max_date}")

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = max_date

    temporal_filtered = apply_date_filter(temporal_df, start_date, end_date)
    payment_filtered = apply_date_filter(payment_df, start_date, end_date)

    payment_agg = (
        payment_filtered.groupby("payment_type", as_index=False)["trips_cnt"].sum().sort_values("trips_cnt", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Trips Distribution by Payment Type")
        categorical_fig = px.bar(
            payment_agg,
            x="payment_type",
            y="trips_cnt",
            labels={"payment_type": "Payment Type", "trips_cnt": "Trips"},
            title="Categorical distribution: trips by payment type",
        )
        categorical_fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(categorical_fig, use_container_width=True)

    with right:
        st.subheader("Daily Trips Trend")
        temporal_fig = px.line(
            temporal_filtered,
            x="trip_date",
            y="trips_cnt",
            labels={"trip_date": "Trip Date", "trips_cnt": "Trips"},
            title="Temporal distribution: daily taxi trips",
        )
        temporal_fig.update_traces(mode="lines")
        st.plotly_chart(temporal_fig, use_container_width=True)


if __name__ == "__main__":
    main()

