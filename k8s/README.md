# Kubernetes (`/k8s`)

Manifestos da **aplicação** (API + migration). O cluster e o banco de dados (Postgres)
são provisionados pelo Terraform em `/infra` - ver `infra/README.md`.

## Pré-requisitos

- Cluster kind já criado e com `kubectl` apontando pra ele (`cd ../infra && terraform apply`).
- `metrics-server` instalado no cluster (necessário para o HPA funcionar; o kind não vem
  com ele por padrão):

  ```bash
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  # kind usa certificados self-signed no kubelet - sem essa flag o metrics-server não
  # consegue coletar métricas e o HPA nunca sai de "unknown".
  kubectl patch deployment metrics-server -n kube-system --type=json \
    -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
  ```

## Imagem da aplicação

Os manifestos apontam para `ghcr.io/leonardo-abe/fiap_tech_challenge_oficina:latest`. Até
existir uma pipeline publicando essa imagem (ver `.github/workflows/`), builde localmente
e carregue direto no cluster kind:

```bash
docker build -t ghcr.io/leonardo-abe/fiap_tech_challenge_oficina:latest ..
kind load docker-image ghcr.io/leonardo-abe/fiap_tech_challenge_oficina:latest --name oficina
```

`deployment.yaml`/`migrate-job.yaml` usam `imagePullPolicy: IfNotPresent` justamente para
usar essa imagem carregada localmente em vez de tentar puxar do registry.

## Aplicar

```bash
kubectl apply -f namespace.yaml

# segredos reais - nunca commitar secret.yaml (já está no .gitignore)
cp secret.yaml.example secret.yaml
# edite secret.yaml com valores reais antes de aplicar
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml

kubectl apply -f migrate-job.yaml
kubectl wait --for=condition=complete job/oficina-migrate -n oficina --timeout=120s

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

kubectl rollout status deployment/oficina-api -n oficina
```

## Testar localmente

```bash
kubectl port-forward svc/oficina-api 8000:8000 -n oficina
curl localhost:8000/health
```

## Gerar carga e observar o HPA escalando

```bash
kubectl get hpa -n oficina -w
# em outro terminal, gere carga contra a API (via port-forward acima ou um pod dentro
# do cluster), por exemplo com k6/hey, ou um loop simples de curl em paralelo.
```

## CD de verdade: runner self-hosted (job `deploy-local` do CI/CD)

O job `deploy-e2e` do workflow (`.github/workflows/ci-cd.yml`) só **valida** que o deploy
funciona, num cluster descartável dentro do runner hospedado do GitHub - nada fica no ar
depois. Para a pipeline realmente **atualizar o cluster que você usa na demonstração** a
cada push na `main` (Continuous Deployment de verdade, não só validação), registre a sua
própria máquina como um runner self-hosted do GitHub Actions:

1. Deixe o cluster de pé (`cd ../infra && terraform apply` - ver `infra/README.md`) e
   mescle o kubeconfig no padrão, para o `kubectl` funcionar sem configuração extra:
   ```bash
   kind export kubeconfig --name oficina
   ```
2. No GitHub: **Settings → Actions → Runners → New self-hosted runner** e siga os
   comandos que a própria página gera para o seu sistema operacional (baixa o agente,
   registra no repositório).
3. Rode o runner (`./run.sh` ou `run.cmd`, conforme o SO) e deixe o processo aberto - é
   ele quem executa o job `deploy-local` sempre que houver um push na `main`.

> **Segurança**: só é seguro manter um runner self-hosted em repositório público porque
> o job `deploy-local` está restrito a `push` direto na `main` - nunca roda em
> `pull_request` (nem de PRs do próprio repositório). Um runner self-hosted exposto a
> `pull_request` de forks seria uma porta aberta para rodar código arbitrário na sua
> máquina a partir de um PR malicioso.

Com o runner rodando, qualquer push na `main` (merge de PR, por exemplo) atualiza
automaticamente a imagem rodando no seu cluster local - é esse fluxo que vale gravar no
vídeo: um `git push`, a aba *Actions* do GitHub executando o job `deploy-local` ao vivo, e
os pods em `kubectl get pods -n oficina -w` sendo substituídos pela nova versão.
