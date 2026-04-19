variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "gcs_bucket_name" {
  type = string
}

variable "raw_dataset" {
  type    = string
  default = "raw"
}

variable "analytics_dataset" {
  type    = string
  default = "analytics"
}

