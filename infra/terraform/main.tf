terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "lake" {
  name                        = var.gcs_bucket_name
  location                    = "US"
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = var.raw_dataset
  location   = "US"
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = var.analytics_dataset
  location   = "US"
}

