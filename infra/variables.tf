variable "aws_region" {
  description = "Região AWS onde o cluster EKS e o Postgres são provisionados."
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Nome do cluster EKS criado por este módulo."
  type        = string
  default     = "oficina"
}

variable "subnet_ids" {
  description = <<-EOT
    Subnets (de pelo menos 2 AZs) onde o cluster EKS e o node group são criados. Sem
    default de propósito - varia por conta/sessão do AWS Academy. Descubra com:
      aws ec2 describe-subnets --filters Name=default-for-az,Values=true \
        --query 'Subnets[].[SubnetId,AvailabilityZone]' --output table
    Atenção: nem toda AZ suporta control plane do EKS (ex.: "us-east-1e" já foi
    rejeitada com UnsupportedAvailabilityZoneException numa conta de teste) - se o
    "apply" falhar com esse erro, troque a subnet pela AZ sugerida na mensagem.
  EOT
  type        = list(string)
}

variable "node_instance_type" {
  description = "Tipo de instância EC2 dos nós do cluster."
  type        = string
  default     = "t3.medium"
}

variable "node_desired_size" {
  description = "Quantidade inicial de nós do node group."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Quantidade mínima de nós do node group."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Quantidade máxima de nós do node group."
  type        = number
  default     = 3
}

variable "kubeconfig_path" {
  description = "Onde o kubeconfig do cluster EKS é escrito/lido."
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
