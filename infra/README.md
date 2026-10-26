# Terraform (`/infra`)

Provisiona um **cluster Kubernetes real na AWS (EKS)** e o **banco de dados Postgres**
dentro dele, usando o **AWS Academy Learner Lab**. A aplicação em si (API) é aplicada
separadamente via `kubectl apply -f ../k8s/` (manual ou pelo CI/CD) - ver `../k8s/README.md`.

## O que é criado

| Recurso | O quê |
|---|---|
| `aws_eks_cluster.this` | Cluster EKS |
| `aws_eks_node_group.this` | Node group (EC2) do cluster, 2 nós `t3.medium` por padrão |
| `null_resource.kubeconfig` | Gera o kubeconfig via `aws eks update-kubeconfig` |
| `null_resource.postgres` | Namespace `oficina`, Secret de credenciais, e o Postgres (`postgres.yaml`: PVC, Deployment, Service) - tudo via `kubectl` |

`role_arn`/`node_role_arn` usam o **`LabRole`** já existente na conta do AWS Academy (o
Learner Lab não permite criar roles IAM novos - por isso reaproveitamos esse).

## ⚠️ Credenciais do AWS Academy expiram

A sessão do Learner Lab dura poucas horas. Antes de rodar qualquer comando abaixo (ou
sempre que receber erro de autenticação/token expirado), pegue credenciais novas em
**AWS Details → AWS CLI** no painel do Academy e exporte:

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
export AWS_DEFAULT_REGION="us-east-1"
```

Se o CI/CD (GitHub Actions) for rodar contra essa mesma conta, esses mesmos 3 valores
também precisam ser atualizados nos **Secrets** do repositório (`Settings → Secrets and
variables → Actions`): `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`.

## Pré-requisitos

- Acesso a um AWS Academy Learner Lab iniciado (credenciais exportadas acima).
- CLIs `aws`, `kubectl` e `terraform` instaladas.

## Bootstrap do backend remoto (uma única vez)

O state do Terraform fica num bucket S3 (não em disco) - diferente do cluster `kind`
efêmero usado antes, o cluster EKS é um recurso real e persistente: sem state remoto,
cada execução do CI (numa VM nova) tentaria recriar o cluster do zero e falharia
(ele já existe na AWS). Esse bucket não pode ser criado pelo próprio Terraform (mesmo
problema de ovo-e-galinha de um backend se auto-provisionar) - crie uma vez, manualmente:

```bash
aws s3 mb s3://oficina-tfstate-$(aws sts get-caller-identity --query Account --output text) --region us-east-1
```

Depois, aponte o backend para esse bucket (substitua pelo nome gerado acima):

```bash
cd infra
terraform init -backend-config="bucket=oficina-tfstate-<account_id>" -backend-config="region=us-east-1"
```

## Aplicar

```bash
cp terraform.tfvars.example terraform.tfvars
# edite terraform.tfvars: senha do Postgres + subnet_ids (ver comentário no arquivo)

terraform apply
```

Uma única `apply` já cria o cluster, o node group **e** o Postgres - nada aqui usa o
provider `kubernetes` do Terraform (que exigiria o endpoint do EKS existir antes mesmo da
primeira `apply` rodar). O cluster/node group são recursos nativos do provider `aws`; o
Postgres é aplicado via `kubectl` (CLI) executado em sequência por `local-exec`, na ordem
certa, dentro da mesma `apply`. Leva de 15 a 20 minutos na primeira vez (criação de
cluster + node group na AWS); execuções seguintes (sem mudança de infraestrutura) são
rápidas, pois o Terraform só confirma que nada mudou.

Para usar `kubectl`/`k8s/README.md` a partir daqui:

```bash
export KUBECONFIG="$(terraform output -raw kubeconfig_path)"
kubectl get nodes
```

Pegue a connection string do banco (para colocar em `../k8s/secret.yaml`) com:

```bash
terraform output -raw postgres_connection_string
```

## 🧨 Destruir tudo (importante — evita cobrança continuada no AWS Academy)

A ordem importa. O Service da API (`../k8s/service.yaml`) é `type: LoadBalancer` - a AWS
cria um Load Balancer real por fora do Terraform quando esse Service é aplicado via
`kubectl`. Se você rodar só `terraform destroy`, esse Load Balancer **fica órfão**,
continua cobrando, e pode até travar a exclusão do cluster/VPC. Siga nesta ordem:

```bash
# 1. Remove a aplicação primeiro - é o que faz a AWS desprovisionar o Load Balancer.
kubectl delete -f ../k8s/

# 2. Só depois destrua a infraestrutura (node group, cluster, Postgres).
terraform destroy
```

Confira que não sobrou nada rodando antes de encerrar a sessão do lab:

```bash
aws eks list-clusters
aws elb describe-load-balancers --query 'LoadBalancerDescriptions[].LoadBalancerName'
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
  --query 'Reservations[].Instances[].InstanceId'
```

Qualquer coisa listada aí ainda está cobrando - repita a limpeza (ou remova manualmente
pelo console) antes de sair.
