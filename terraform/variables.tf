variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for all resources"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "Name of the GKE Autopilot cluster"
  type        = string
  default     = "diet-optimizer-cluster"
}

variable "github_repo_owner" {
  description = "GitHub repository owner (user or organization)"
  type        = string
}

variable "github_repo_name" {
  description = "GitHub repository name"
  type        = string
  default     = "api-diet-optimizer"
}
