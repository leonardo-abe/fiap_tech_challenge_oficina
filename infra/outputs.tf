output "kubeconfig_path" {
  description = "Use com 'export KUBECONFIG=<valor>' ou 'kubectl --kubeconfig <valor>' para falar com o cluster criado."
  value       = var.kubeconfig_path
}

output "postgres_connection_string" {
  description = "DATABASE_URL para colocar em k8s/secret.yaml (ver k8s/README.md)."
  value       = "postgresql+asyncpg://${var.postgres_user}:${var.postgres_password}@postgres.${kubernetes_namespace.oficina.metadata[0].name}.svc.cluster.local:5432/${var.postgres_db}"
  sensitive   = true
}
