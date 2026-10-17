# Terraform (`/infra`)

Provisiona o **cluster Kubernetes local (kind)** e o **banco de dados Postgres** dentro
dele. A aplicação em si (API) é aplicada separadamente via `kubectl apply -f ../k8s/`
(manual ou pelo CI/CD) - ver `../k8s/README.md`.

## O que é criado

| Recurso | O quê |
|---|---|
| `null_resource.kind_cluster` | Cluster kind local (via CLI `kind`), definido por `kind-config.yaml` |
| `null_resource.postgres` | Namespace `oficina`, Secret de credenciais, e o Postgres propriamente dito (`postgres.yaml`: PVC, Deployment, Service) - tudo via `kubectl` |

## Pré-requisitos

- Docker rodando.
- CLIs `kind`, `kubectl` e `terraform` instaladas.

## Aplicar

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
# edite terraform.tfvars com uma senha de verdade

terraform init
terraform apply
```

Uma única `apply` já cria o cluster **e** o Postgres: nada aqui usa o provider
`kubernetes` do Terraform (que exigiria o cluster existir antes mesmo da primeira
`apply` rodar, forçando duas passadas). O cluster (`kind`) e o banco (`kubectl`) são
criados por comandos de CLI executados em sequência via `local-exec`, na ordem certa,
dentro da mesma `apply`.

Isso cria o cluster `oficina` e escreve o kubeconfig em `kubeconfig` (não commitado).
Para usar `kubectl`/`k8s/README.md` a partir daqui:

```bash
export KUBECONFIG="$(terraform output -raw kubeconfig_path)"
kubectl get nodes
```

Pegue a connection string do banco (para colocar em `../k8s/secret.yaml`) com:

```bash
terraform output -raw postgres_connection_string
```

## Destruir

```bash
terraform destroy
```

Remove o Postgres e depois o cluster kind inteiro (não há nada para "sobrar" entre uma
execução e outra - o Postgres local não guarda dado real).
