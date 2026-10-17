terraform {
  required_version = ">= 1.5.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.31"
    }
  }
}

# o provider só precisa do kubeconfig gerado pelo "kind create cluster" em main.tf; a
# conexão real só acontece quando algum recurso kubernetes_* é aplicado (depends_on
# garante que isso só ocorre depois que o cluster existe).
provider "kubernetes" {
  config_path = var.kubeconfig_path
}
