# Dashboard (Streamlit)

This dashboard uses BigQuery marts created by the pipeline:

- `analytics.mart_payment_type_daily` (categorical tile)
- `analytics.mart_trips_daily` (temporal tile)

Replace `<your_project_id>` in the run command below with your own GCP project id. If you also changed the dataset name from the repository default, update `ANALYTICS_DATASET` accordingly.

## Tiles

1. **Trips Distribution by Payment Type**
2. **Daily Trips Trend**

Both tiles include chart titles and axis labels, and share one date filter.

## Run locally

```bash
PYTHONPATH=src GCP_PROJECT_ID=<your_project_id> ANALYTICS_DATASET=analytics python -m streamlit run dashboard/app.py
```

## Share with peers

- Option A: Streamlit Community Cloud deployment URL
- Option B: Record a walkthrough and share local run screenshot in `docs/dashboard.png`

Any concrete project id shown in screenshots is only a demo value from my environment and is not required for a reviewer to run the dashboard locally.


