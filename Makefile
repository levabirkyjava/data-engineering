PYTHON ?= python3

.PHONY: test

test:
	$(PYTHON) -m pytest -q

.PHONY: run-preview
run-preview:
	PYTHONPATH=src GCP_PROJECT_ID=$${GCP_PROJECT_ID:-demo-project} DBT_BIGQUERY_PROJECT=$${DBT_BIGQUERY_PROJECT:-demo-project} $(PYTHON) scripts/preview_queries.py

.PHONY: compose-config
compose-config:
	docker compose config > /tmp/chicago-taxi-compose.out

.PHONY: smoke
smoke: test run-preview

.PHONY: run-dashboard
run-dashboard:
	PYTHONPATH=src GCP_PROJECT_ID=$${GCP_PROJECT_ID:-demo-project} ANALYTICS_DATASET=$${ANALYTICS_DATASET:-analytics} $(PYTHON) -m streamlit run dashboard/app.py

