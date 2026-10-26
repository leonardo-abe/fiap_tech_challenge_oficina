terraform {
  required_version = ">= 1.5.0"

  # state local (sem backend remoto) de propósito - este Terraform roda manualmente, uma
  # única vez (ver infra/README.md), para provisionar o cluster/node group/Postgres. O
  # CI/CD não executa "terraform apply": um deploy normal só troca a imagem da aplicação
  # via kubectl (ver .github/workflows/ci-cd.yml), nunca mexe na infraestrutura - por
  # isso não há necessidade de state remoto compartilhado entre execuções.

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
