# Crossplane
resource "helm_release" "crossplane" {
  name             = "crossplane"
  namespace        = "crossplane-system"
  create_namespace = true
  repository       = "https://charts.crossplane.io/stable"
  chart            = "crossplane"
  version          = "1.15.0"

  set {
    name  = "args"
    value = "{--enable-usages}"
  }

  depends_on = [google_container_cluster.autopilot]
}

# KEDA
resource "helm_release" "keda" {
  name             = "keda"
  namespace        = "keda"
  create_namespace = true
  repository       = "https://kedacore.github.io/charts"
  chart            = "keda"
  version          = "2.13.1"

  timeout    = 600

  depends_on = [google_container_cluster.autopilot]
}

# KEDA HTTP Add-on
resource "helm_release" "keda_http_addon" {
  name             = "keda-http-addon"
  namespace        = "keda"
  create_namespace = false
  repository       = "https://kedacore.github.io/charts"
  chart            = "keda-add-ons-http"
  version          = "0.8.0"

  depends_on = [helm_release.keda]
}

# Argo CD
resource "helm_release" "argocd" {
  name             = "argocd"
  namespace        = "argocd"
  create_namespace = true
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "6.4.0"

  # Minimal resource configuration for cost efficiency
  set {
    name  = "server.resources.requests.cpu"
    value = "100m"
  }
  set {
    name  = "server.resources.requests.memory"
    value = "128Mi"
  }
  set {
    name  = "controller.resources.requests.cpu"
    value = "100m"
  }
  set {
    name  = "controller.resources.requests.memory"
    value = "128Mi"
  }
  set {
    name  = "repoServer.resources.requests.cpu"
    value = "100m"
  }
  set {
    name  = "repoServer.resources.requests.memory"
    value = "128Mi"
  }

  depends_on = [google_container_cluster.autopilot]
}
