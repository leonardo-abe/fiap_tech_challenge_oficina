terraform {
  required_version = ">= 1.5.0"

  # state remoto (S3 + DynamoDB) - diferente do cluster kind efêmero de antes, o cluster
  # EKS é um recurso real e persistente na AWS: sem state remoto, cada execução do CI
  # (numa VM nova do runner hospedado, sem state local) tentaria criar o cluster de novo
  # e falharia porque ele já existe. O bucket/tabela são criados manualmente uma única vez
  # (ver infra/README.md) - o próprio backend não pode ser gerenciado por este Terraform
  # (mesmo problema de ovo-e-galinha de um backend se auto-provisionar).
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
