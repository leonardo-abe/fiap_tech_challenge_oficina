# Terraform (`/infra`)

Provisiona o **cluster Kubernetes local (kind)** e o **banco de dados Postgres** dentro
dele. A aplicação em si (API) é aplicada separadamente via `kubectl apply -f ../k8s/`
(manual ou pelo CI/CD) - ver `../k8s/README.md`.

## O que é criado

| Recurso | O quê |
|---|---|
| `null_resource.kind_cluster` | Cluster kind local (via CLI `kind`), definido por `kind-config.yaml` |
| `kubernetes_namespace.oficina` | Namespace `oficina` |
| `kubernetes_secret.postgres` | Credenciais do Postgres |
| `kubernetes_persistent_volume_claim.postgres` | Volume persistente de 1Gi pros dados do Postgres |
| `kubernetes_deployment.postgres` | Postgres 16 (1 réplica) |
| `kubernetes_service.postgres` | Service `postgres` (porta 5432) - é o host usado em `DATABASE_URL` |

## Pré-requisitos

- Docker rodando.
- CLIs `kind`, `kubectl` e `terraform` instaladas.

## Aplicar

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
# edite terraform.tfvars com uma senha de verdade

terraform init
terraform apply -target=null_resource.kind_cluster   # 1/2: só o cluster
terraform apply                                       # 2/2: namespace + Postgres
```

> **Por que em duas etapas?** O provider `kubernetes` só consegue ler o kubeconfig
> depois que o cluster kind existe, mas ele é configurado/validado já na primeira
> passada de um único `apply` - rodar tudo de uma vez faz os recursos do Postgres
> falharem com erro de conexão, porque o kubeconfig ainda não existe no momento em que
> o provider tenta usá-lo. O primeiro `apply`, restrito a `null_resource.kind_cluster`
> via `-target`, cria só o cluster (e o kubeconfig); o segundo aplica o restante sem
> problema. É uma limitação conhecida de providers Terraform que dependem de outro
> recurso criado na mesma `apply` (não é um bug deste módulo) - por isso o uso de
> `-target` aqui é intencional, apesar do aviso do Terraform de que não é para uso
> rotineiro.

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
