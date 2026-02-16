Context

 The diet-optimizer API is a lightweight, stateless FastAPI application (~712KB) that solves diet optimization problems using SciPy linear programming. It currently has a
 Dockerfile and docker-compose but no Kubernetes manifests, Helm charts, or CI/CD. The goal is to deploy it to GKE Autopilot with true scale-to-zero for cost efficiency
 (~$10-15/mo), using a fully declarative, zero-credentials approach:

 - Terraform creates the GKE Autopilot cluster + Workload Identity bindings (the one thing that must exist before Crossplane can run)
 - Crossplane (inside the cluster) declaratively manages remaining GCP resources (static IP, Artifact Registry)
 - Helm packages the application
 - KEDA provides HTTP-based scale-to-zero
 - Argo CD provides GitOps continuous deployment
 - GitHub Actions provides CI (image builds only)
 - Workload Identity everywhere — zero stored credential files

 ---
 Architecture Stack

 ┌──────────────────────┬──────────────────────────────┬──────────────────────────────────────────────────────────────┐
 │        Layer         │             Tool             │                           Purpose                            │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Cluster Provisioning │ Terraform                    │ Declaratively create GKE Autopilot + IAM + Workload Identity │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ GCP Resource Mgmt    │ Crossplane (Upjet GCP)       │ Declarative static IP + Artifact Registry from inside K8s    │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ App Packaging        │ Helm                         │ Templatized K8s manifests for the API                        │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Autoscaling          │ KEDA + HTTP Add-on           │ Scale 0-3 pods based on HTTP traffic                         │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ CD (Deploy)          │ Argo CD                      │ GitOps - watches repo, syncs to cluster                      │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ CI (Build)           │ GitHub Actions               │ Build Docker image, push to Artifact Registry, update tag    │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Networking           │ GCP Network LB + Static IP   │ Stable external endpoint                                     │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Auth (CI)            │ Workload Identity Federation │ GitHub Actions authenticates to GCP via OIDC — no SA keys    │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Auth (Crossplane)    │ GKE Workload Identity        │ Crossplane pod authenticates to GCP via K8s SA — no SA keys  │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Secrets (optional)   │ Google Secret Manager        │ For any future app-level secrets                             │
 ├──────────────────────┼──────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Local Testing        │ minikube                     │ Test Helm chart + Dockerfile locally before deploying to GCP │
 └──────────────────────┴──────────────────────────────┴──────────────────────────────────────────────────────────────┘

 ---
 Estimated Monthly Cost

 ┌──────────────────────────────────────────────────┬────────────────┬─────────────────────────────────────┐
 │                     Resource                     │      Cost      │                Notes                │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ GKE Autopilot cluster fee                        │ ~$6.85         │ Flat management fee                 │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Compute (scale-to-zero, active ~4hr/day)         │ ~$2-5          │ 0.5 vCPU + 512MB only when pods run │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Always-on components (KEDA interceptor, Argo CD) │ Included above │ ~0.5 vCPU + 512MB total             │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Static IP (attached to LB)                       │ ~$0-1.46       │ Free when in use, ~$1.46 when idle  │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Artifact Registry storage                        │ ~$0.10         │ Docker images                       │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Google Secret Manager                            │ ~$0            │ Free tier covers 10K accesses/mo    │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Network egress                                   │ ~$0.01-1       │ STANDARD tier, minimal traffic      │
 ├──────────────────────────────────────────────────┼────────────────┼─────────────────────────────────────┤
 │ Total                                            │ ~$10-14/mo     │                                     │
 └──────────────────────────────────────────────────┴────────────────┴─────────────────────────────────────┘

 ---
 New Branch

 Create branch feature/gke-deployment from main.

 ---
 Repository Structure (new files only)

 api-diet-optimizer/
 ├── .github/workflows/
 │   └── ci.yml                          # GitHub Actions CI: build, push, update tag
 │
 ├── terraform/
 │   ├── main.tf                         # GKE Autopilot cluster + GCP APIs
 │   ├── variables.tf                    # Input variables (no defaults for sensitive values)
 │   ├── outputs.tf                      # Cluster endpoint, static IP, registry URL
 │   ├── iam.tf                          # Service accounts + Workload Identity bindings
 │   ├── providers.tf                    # google, google-beta, kubernetes, helm providers
 │   ├── helm-releases.tf               # Crossplane, KEDA, Argo CD installed via Helm provider
 │   ├── terraform.tfvars.example        # Template (committed) - no real GCP values
 │   ├── terraform.tfvars                # Actual values (GITIGNORED)
 │   ├── backend.tf                      # GCS remote state (optional)
 │   └── .terraform.lock.hcl            # Lock file (committed)
 │
 ├── crossplane/
 │   ├── provider-config.yaml            # GCP ProviderConfig using Workload Identity
 │   ├── static-ip.yaml                  # Regional external IP (uses envsubst placeholders)
 │   └── artifact-registry.yaml          # Docker repo (uses envsubst placeholders)
 │
 ├── helm/diet-optimizer/
 │   ├── Chart.yaml
 │   ├── values.yaml                     # Defaults (no secrets)
 │   ├── values-prod.yaml                # Production overrides (image tag updated by CI)
 │   └── templates/
 │       ├── _helpers.tpl
 │       ├── deployment.yaml
 │       ├── service.yaml                # ClusterIP (internal) + LoadBalancer (external via interceptor)
 │       ├── httpscaledobject.yaml        # KEDA HTTP scale-to-zero config
 │       └── configmap.yaml
 │
 ├── argocd/
 │   └── application.yaml                # Argo CD Application definition
 │
 ├── docs/
 │   └── DEPLOYMENT.md                   # Deployment strategy doc with Mermaid diagrams + links
 │
 └── .gitignore                          # UPDATE: add terraform/.terraform/, terraform/terraform.tfvars, etc.


 ---
 Implementation Steps

 Pre-Step: Create PROMPT.md

 - Create PROMPT.md in the repo root containing the full deployment plan as a reference document
 - This serves as the canonical prompt/instructions document for the entire GKE deployment
 - Includes: architecture, steps, cost breakdown, Mermaid diagrams, and all implementation details
 - Created BEFORE any other implementation work begins

 Step 0: Local prerequisites + minikube

 - Verify/install required CLI tools: terraform, helm, kubectl, gcloud, envsubst
 - Install minikube if not present (via brew install minikube)
 - Start minikube: minikube start
 - Local Helm validation: Run helm lint and helm template against minikube to test the chart renders correctly
 - Local deployment test: Deploy the Helm chart to minikube (without KEDA/Crossplane/ArgoCD) using helm install diet-optimizer helm/diet-optimizer -f
 helm/diet-optimizer/values.yaml with scaling.enabled=false and service.type=NodePort
 - Verify the API works locally on minikube: minikube service diet-optimizer-internal --url → curl <url>/health
 - This validates the Helm chart and Dockerfile work correctly before touching GCP
 - Stop minikube when done: minikube stop

 Step 1: Branch + repo scaffolding

 - Create feature/gke-deployment branch
 - Add to .gitignore:
 terraform/.terraform/
 terraform/terraform.tfvars
 terraform/*.tfstate*
 terraform/.terraform.lock.hcl
 - Create all directories: terraform/, crossplane/, helm/diet-optimizer/templates/, argocd/, docs/
 - Create terraform/terraform.tfvars.example with placeholder values

 Step 2: Terraform configuration

 - providers.tf: google, google-beta, kubernetes, helm providers
 - variables.tf: project_id, region, cluster_name, github_repo_owner, github_repo_name
 - main.tf:
   - Enable GCP APIs (container, compute, artifactregistry, iam, iamcredentials, secretmanager)
   - Create GKE Autopilot cluster (regular release channel)
   - Get cluster credentials for kubernetes/helm providers
 - iam.tf:
   - Create GCP SA for Crossplane (crossplane-sa) with roles: compute.networkAdmin, artifactregistry.admin
   - Bind Crossplane SA to K8s SA via GKE Workload Identity (crossplane-system/crossplane K8s SA → crossplane-sa GCP SA)
   - Create GCP SA for GitHub Actions (github-actions-sa) with role: artifactregistry.writer
   - Create Workload Identity Pool + OIDC Provider for GitHub Actions
   - Bind GitHub repo to GitHub Actions SA via Workload Identity Federation
 - helm-releases.tf:
   - Install Crossplane via Helm provider (namespace: crossplane-system)
   - Install KEDA + HTTP add-on via Helm provider (namespace: keda)
   - Install Argo CD via Helm provider (namespace: argocd, minimal resources)
 - outputs.tf: cluster name, WIF provider ID, GitHub Actions SA email, Crossplane SA email
 - backend.tf: Optional GCS bucket for remote state (can start with local state)

 Step 3: Crossplane manifests

 - provider-config.yaml: Uses InjectedIdentity credential source (GKE Workload Identity — no SA key)
 spec:
   credentials:
     source: InjectedIdentity  # Uses the K8s SA's bound GCP identity
 - static-ip.yaml: compute.gcp.upbound.io/v1beta1/Address, STANDARD network tier, ${GCP_REGION} placeholder
 - artifact-registry.yaml: Docker format repository, ${GCP_REGION} placeholder
 - Applied post-Terraform via envsubst < file.yaml | kubectl apply -f -

 Step 4: Helm chart

 - Chart.yaml, values.yaml, values-prod.yaml
 - Templates:
   - _helpers.tpl: Labels, selectors, image reference helpers
   - deployment.yaml: Python 3.11-slim image, port 8000, 250m/256Mi requests, 500m/512Mi limits, health probes at /health, no replicas field (KEDA manages it)
   - service.yaml: Two services:
       i. ClusterIP diet-optimizer-internal → app pods (used by KEDA interceptor to forward)
     ii. LoadBalancer diet-optimizer-external → KEDA HTTP interceptor proxy (with static IP annotation)
   - httpscaledobject.yaml: min=0, max=3, scaledownPeriod=300s, requestRate target=10/s, window=1m
   - configmap.yaml: LOG_LEVEL, WORKERS, PORT
 - Validate with helm lint and helm template

 Step 5: GitHub Actions CI

 - .github/workflows/ci.yml:
   - Trigger: push to main, paths filter **/*.py, Dockerfile, pyproject.toml (prevents CI loop)
   - Auth: google-github-actions/auth@v2 with Workload Identity Federation (id-token permission)
   - Steps: checkout → GCP auth via WIF → login to Artifact Registry → build image → push with SHA tag → sed update values-prod.yaml tag → commit + push
   - Zero stored secrets: WIF provider ID and SA email are the only GitHub Secrets needed (non-sensitive identifiers, not credentials)

 Step 6: Argo CD Application

 - argocd/application.yaml:
   - Watches helm/diet-optimizer path on main branch
   - Auto-sync with prune + selfHeal
   - Creates diet-optimizer namespace
   - Value files: values.yaml + values-prod.yaml

 Step 7: Deployment strategy doc (docs/DEPLOYMENT.md)

 - Architecture overview with 4 Mermaid diagrams:
   a. Architecture components diagram
   b. CI/CD sequence flow
   c. HTTP request flow (user → static IP → LB → interceptor → pod)
   d. Scale-to-zero state machine
 - Cost breakdown table
 - Prerequisites & setup instructions (Terraform apply, Crossplane apply, initial image push)
 - Hyperlinks to: GKE Autopilot, KEDA, Crossplane, Argo CD, Helm, Workload Identity, Terraform GCP docs
 - Secrets management guide (Workload Identity explanation)
 - Troubleshooting section

 Step 8: Deploy + validate (live infrastructure)

 1. cd terraform && terraform init && terraform plan && terraform apply — creates cluster, IAM, installs Crossplane/KEDA/ArgoCD
 2. gcloud container clusters get-credentials <cluster> --region <region> — configure kubectl
 3. Apply Crossplane managed resources: envsubst < crossplane/static-ip.yaml | kubectl apply -f - (and artifact-registry)
 4. Wait for Crossplane to provision: kubectl get address.compute.gcp.upbound.io/diet-optimizer-ip
 5. Update values-prod.yaml with static IP and Artifact Registry URL
 6. Push initial Docker image: docker build && docker push
 7. Apply Argo CD app: kubectl apply -f argocd/application.yaml
 8. Verify: curl http://<static-ip>/health → 200
 9. Test scale-to-zero: wait 5min → 0 pods → send request → pod scales up in ~5-10s
 10. Test CI/CD: push Python change → GH Actions builds → Argo CD deploys

 ---
 Key Design Decisions

 1. Terraform for cluster, Crossplane for GCP resources: Terraform handles the chicken-and-egg problem (creating the cluster + installing Crossplane/KEDA/ArgoCD). Crossplane
 then declaratively manages GCP resources (static IP, Artifact Registry) from inside the cluster with automatic drift detection.
 2. Zero stored credentials:
   - GitHub Actions → GCP: Workload Identity Federation (OIDC token exchange, no SA key)
   - Crossplane → GCP: GKE Workload Identity (K8s SA bound to GCP SA, no SA key)
   - Result: No JSON key files anywhere — not in GitHub, not in K8s Secrets, not on disk
 3. KEDA HTTP Add-on routing: LoadBalancer Service targets the KEDA interceptor proxy (not app pods). Interceptor buffers requests during scale-from-zero, forwards to app's
 internal ClusterIP once pods are ready. Cold start ~5-10s.
 4. CI feedback loop prevention: GitHub Actions triggers only on *.py / Dockerfile / pyproject.toml changes. The CI's commit to values-prod.yaml (YAML) doesn't re-trigger.
 5. STANDARD network tier for static IP — cheaper than PREMIUM, sufficient for regional IP-only access.
 6. GCP values not in repo: Terraform uses terraform.tfvars (gitignored). Crossplane YAML uses envsubst placeholders. values-prod.yaml will contain the static IP and registry
 URL after setup (these are public infrastructure info, not secrets).

 ---
 Verification Plan

 Local (minikube):
 1. minikube start — cluster running
 2. helm lint helm/diet-optimizer — chart validates
 3. helm install diet-optimizer helm/diet-optimizer --set scaling.enabled=false --set service.type=NodePort — deploys to minikube
 4. curl $(minikube service diet-optimizer-internal --url)/health — returns 200
 5. helm uninstall diet-optimizer && minikube stop

 GCP:
 6. terraform plan — shows expected resources without errors
 3. After apply: kubectl get pods -n keda, -n argocd, -n crossplane-system — all Running
 4. kubectl get address.compute.gcp.upbound.io/diet-optimizer-ip — shows provisioned IP
 5. curl http://<static-ip>/health — returns 200
 6. curl -X POST http://<static-ip>/optimize -H 'Content-Type: application/json' -d @example_request.json — returns optimization result
 7. Wait 5+ minutes with no traffic → kubectl get pods -n diet-optimizer shows 0 pods
 8. Send request again → pod scales up within 5-10s, returns result
 9. Push a Python change to main → GitHub Actions builds image → Argo CD deploys new version
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌