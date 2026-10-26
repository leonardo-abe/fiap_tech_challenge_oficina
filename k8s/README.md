# Kubernetes (`/k8s`)

Manifestos da **aplicação** (API + migration). O cluster (EKS) e o banco de dados
(Postgres) são provisionados pelo Terraform em `/infra` - ver `infra/README.md`,
inclusive a seção de credenciais do AWS Academy e a ordem certa de destroy.

## Pré-requisitos

- Cluster já criado e com `kubectl` apontando pra ele (`cd ../infra && terraform apply`,
  depois `export KUBECONFIG="$(terraform output -raw kubeconfig_path)"`).
- `metrics-server` instalado no cluster (necessário para o HPA funcionar; o EKS não vem
  com ele por padrão):

  ```bash
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  ```

## Imagem da aplicação

Os manifestos apontam para `ghcr.io/leonardo-abe/fiap_tech_challenge_oficina:local` - é só
um placeholder de template (não "latest" de propósito, por rastreabilidade); o CI/CD
substitui pela tag do commit (SHA) antes de aplicar (ver `.github/workflows/ci-cd.yml`).
O pacote no GHCR é público, então o node do EKS consegue puxar a imagem direto do
registry sem credencial nenhuma.

## Aplicar

```bash
kubectl apply -f namespace.yaml

# segredos reais - nunca commitar secret.yaml (já está no .gitignore)
cp secret.yaml.example secret.yaml
# edite secret.yaml com valores reais antes de aplicar (DATABASE_URL vem de
# "terraform output -raw postgres_connection_string" em /infra)
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml

kubectl apply -f migrate-job.yaml
kubectl wait --for=condition=complete job/oficina-migrate -n oficina --timeout=120s

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

kubectl rollout status deployment/oficina-api -n oficina
```

## Acessar a API (público, via Load Balancer)

`service.yaml` é `type: LoadBalancer` - a AWS provisiona um Load Balancer real com IP/DNS
público (leva alguns minutos para ficar pronto):

```bash
kubectl get svc oficina-api -n oficina -w
# espere a coluna EXTERNAL-IP deixar de ser "<pending>"

curl http://<EXTERNAL-IP>:8000/health
```

## Gerar carga e observar o HPA escalando

```bash
kubectl get hpa -n oficina -w
# em outro terminal, gere carga contra o EXTERNAL-IP acima, por exemplo com k6/hey, ou
# um loop simples de curl em paralelo.
```

## CD de verdade: pipeline do GitHub Actions mirando a nuvem

O job `deploy` do workflow (`.github/workflows/ci-cd.yml`) roda num runner hospedado
comum do GitHub (não precisa de runner self-hosted, já que o alvo é um cluster na nuvem
alcançável pela internet) e atualiza **o mesmo cluster EKS persistente** a cada push na
`main`: autentica na AWS com os secrets do repositório, roda
`terraform apply` em `/infra` (idempotente - depois da primeira vez, só confirma que
nada mudou) e aplica os manifestos deste diretório com a tag da imagem recém-publicada,
em steps separados e nomeados (namespace/configmap, secret, migration, deployment/
service/HPA, smoke test) - fácil de acompanhar passo a passo na aba *Actions* do GitHub.
O último step busca e publica a URL pública da API (Load Balancer) direto no resumo da
execução (`Summary` da run no Actions).

**Antes de cada execução** (ou sempre que a sessão do AWS Academy expirar - dura poucas
horas), atualize os secrets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e
`AWS_SESSION_TOKEN` em `Settings → Secrets and variables → Actions` com as credenciais
atuais do Learner Lab (aba **AWS Details → AWS CLI**). Sem isso, o job falha na
autenticação - é esperado, não é um bug: é o trade-off documentado de usar um ambiente de
laboratório com credenciais temporárias em vez de uma conta AWS permanente.

### Secrets necessários no repositório (`Settings → Secrets and variables → Actions`)

| Secret | O quê | Muda a cada sessão do Academy? |
|---|---|---|
| `AWS_ACCESS_KEY_ID` | Credencial temporária do Learner Lab | Sim |
| `AWS_SECRET_ACCESS_KEY` | Credencial temporária do Learner Lab | Sim |
| `AWS_SESSION_TOKEN` | Credencial temporária do Learner Lab | Sim |
| `TF_STATE_BUCKET` | Nome do bucket S3 do backend remoto do Terraform (ver `infra/README.md`) | Não |
| `AWS_SUBNET_IDS` | Lista de subnets, formato `["subnet-a","subnet-b","subnet-c"]` (ver `infra/README.md`) | Normalmente não (só se a conta do lab mudar) |
| `POSTGRES_PASSWORD` | Senha do Postgres (mesma usada no `terraform.tfvars` em `/infra`) | Não |
| `JWT_SECRET_KEY` | Segredo de assinatura dos JWTs da API | Não |
| `SEED_ADMIN_SENHA` / `SEED_ATENDENTE_SENHA` / `SEED_MECANICO_SENHA` | Senhas dos usuários de seed criados pela API | Não |

Só os três primeiros (credenciais AWS) precisam ser atualizados periodicamente; os
demais são configurados uma única vez.

Com os secrets em dia, qualquer push na `main` (merge de PR, por exemplo) atualiza
automaticamente a imagem rodando no cluster - é esse fluxo que vale gravar no vídeo: um
`git push`, a aba *Actions* do GitHub executando o job `deploy` ao vivo, e os pods em
`kubectl get pods -n oficina -w` sendo substituídos pela nova versão, acessível
publicamente pelo `EXTERNAL-IP` do Service.
