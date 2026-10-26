terraform {
  required_version = ">= 1.5.0"

  # state remoto (S3) - o job "deploy" do CI/CD roda "terraform apply" a cada push (ver
  # .github/workflows/ci-cd.yml), para que o Terraform fique exercitado de ponta a ponta
  # pela pipeline, não só localmente. Isso exige state compartilhado: sem ele, cada
  # execução (numa VM nova do runner hospedado, sem o state local) acharia que nada foi
  # criado ainda e tentaria recriar o cluster, que já existe - e falharia. Com state
  # remoto, essas execuções (depois da primeira) só confirmam que nada mudou - rápido,
  # idempotente. O bucket é criado manualmente uma única vez (ver infra/README.md) - o
  # próprio backend não pode ser gerenciado por este Terraform (mesmo problema de
  # ovo-e-galinha de um backend se auto-provisionar).
  backend "s3" {
    key     = "oficina/terraform.tfstate"
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# nenhum provider "kubernetes" aqui de propósito - o endpoint do EKS só existe depois do
# cluster criado, o que reintroduziria o mesmo problema de bootstrapping já visto (e já
# resolvido) com o provider "kubernetes" na época do kind: ele tentaria se conectar antes
# do cluster existir, forçando duas passadas de "apply". Em vez disso, tudo que fala com
# a API do cluster (namespace, secret, Postgres) roda via "kubectl" por local-exec, depois
# que o cluster e o kubeconfig já existem (ver main.tf e postgres.tf).
