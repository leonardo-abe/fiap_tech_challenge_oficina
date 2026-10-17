terraform {
  required_version = ">= 1.5.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# nenhum provider além do "null" é necessário - tudo (cluster kind, namespace, secret,
# Postgres) é criado via "kubectl"/"kind" executados por local-exec (ver main.tf e
# postgres.tf), não por recursos típicos de um provider que precisaria se conectar à
# API do cluster já na configuração do provider (o que exigiria o cluster existir
# antes mesmo do primeiro "terraform apply" rodar).
