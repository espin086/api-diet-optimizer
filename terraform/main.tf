# Enable required GCP APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "container.googleapis.com",
    "compute.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "secretmanager.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# GKE Autopilot cluster
resource "google_container_cluster" "autopilot" {
  name     = var.cluster_name
  location = var.region
  project  = var.project_id

  enable_autopilot = true

  release_channel {
    channel = "REGULAR"
  }

  # Workload Identity is enabled by default on Autopilot
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Network configuration
  network    = "default"
  subnetwork = "default"

  # Deletion protection (disable for dev/testing)
  deletion_protection = false

  depends_on = [google_project_service.apis]
}
