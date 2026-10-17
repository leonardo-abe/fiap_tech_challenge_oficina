variable "cluster_name" {
  description = "Nome do cluster kind local criado por este módulo."
  type        = string
  default     = "oficina"
}

variable "kubeconfig_path" {
  description = "Onde o kubeconfig do cluster kind é escrito/lido."
  type        = string
  default     = "kubeconfig"
}

variable "postgres_user" {
  description = "Usuário do Postgres provisionado no cluster."
  type        = string
  default     = "oficina"
}

variable "postgres_db" {
  description = "Nome do banco Postgres provisionado no cluster."
  type        = string
  default     = "oficina"
}

variable "postgres_password" {
  description = "Senha do Postgres - sem default proposital, defina em terraform.tfvars (nunca commitado, ver .gitignore)."
  type        = string
  sensitive   = true
}
