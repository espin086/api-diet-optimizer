# Uncomment to use GCS remote state backend.
# First create the bucket: gsutil mb -p <PROJECT_ID> gs://<PROJECT_ID>-terraform-state
#
# terraform {
#   backend "gcs" {
#     bucket = "YOUR_PROJECT_ID-terraform-state"
#     prefix = "diet-optimizer"
#   }
# }
