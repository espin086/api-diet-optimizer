output "cluster_name" {
  description = "GKE Autopilot cluster name"
  value       = google_container_cluster.autopilot.name
}

output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.autopilot.endpoint
  sensitive   = true
}

output "cluster_location" {
  description = "GKE cluster location"
  value       = google_container_cluster.autopilot.location
}

output "wif_provider_id" {
  description = "Workload Identity Federation provider ID for GitHub Actions"
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "github_actions_sa_email" {
  description = "GitHub Actions service account email"
  value       = google_service_account.github_actions.email
}

output "crossplane_sa_email" {
  description = "Crossplane service account email"
  value       = google_service_account.crossplane.email
}
