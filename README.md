# Oficina Mecânica API

## Descrição

Backend do **Sistema Integrado de Atendimento e Execução de Serviços** de uma oficina
mecânica de médio porte — projeto da Fase 1 do Tech Challenge (Pós-Tech Software
Architecture, FIAP). Substitui o controle manual/planilhas por uma API que cobre
atendimento, diagnóstico, execução de serviços e entrega de veículos.

## Visão geral

A oficina não tinha como priorizar atendimentos, controlar estoque de peças ou dar ao
cliente visibilidade do andamento do serviço. Esta API resolve isso com:

- Cadastro de clientes (validado por CPF/CNPJ), veículos (placa validada) e catálogo de
  serviços/peças, com controle de estoque.
- Criação de Ordem de Serviço (OS) com orçamento calculado automaticamente a partir dos
  serviços e peças incluídos — nunca digitado manualmente.
- Acompanhamento da OS por uma máquina de estados no próprio domínio (`RECEBIDA` →
  `EM_DIAGNOSTICO` → `AGUARDANDO_APROVACAO` → `EM_EXECUCAO` → `FINALIZADA` → `ENTREGUE`,
  além de `REPROVADA`/`CANCELADA`), com notificação por e-mail ao cliente quando o
  orçamento fica pronto para aprovação.
- Consulta pública de status da OS pelo cliente (sem autenticação, validada por
  CPF/CNPJ) e relatório de tempo médio de execução dos serviços.
- Autenticação JWT com RBAC (`ADMIN`/`ATENDENTE`/`MECANICO`) para as rotas
  administrativas.

## Documentação

- [docs/arquitetura.md](docs/arquitetura.md) — camadas (Clean Architecture), regra de
  dependência, Domain-Driven Design aplicado (entidades, Value Objects, aggregate,
  máquina de estados da OS) e portas/adapters.
- [docs/linguagem-ubiqua.md](docs/linguagem-ubiqua.md) — glossário dos termos de negócio
  e onde cada um vive no código.
- [docs/banco-de-dados.md](docs/banco-de-dados.md) — justificativa da escolha do
  PostgreSQL.
- [docs/relatorio-vulnerabilidades.md](docs/relatorio-vulnerabilidades.md) — scan de
  vulnerabilidades (SAST/SCA) e cobertura por categoria do OWASP Top 10.

## Tecnologias

- **Linguagem/runtime**: Python 3.12
- **Framework web**: FastAPI + Uvicorn
- **Banco de dados**: PostgreSQL 16, via SQLAlchemy 2.0 assíncrono (`asyncpg`) — ver
  [justificativa da escolha](docs/banco-de-dados.md)
- **Migrações**: Alembic
- **Autenticação**: JWT (`PyJWT`) + `bcrypt` para hash de senha
- **Validação**: Pydantic v2 / `pydantic-settings`, `validate-docbr` (CPF/CNPJ)
- **Rate limiting**: `slowapi`
- **Gerenciador de pacotes**: [uv](https://docs.astral.sh/uv/)
- **Containers**: Docker + Docker Compose
- **Testes**: pytest, `pytest-asyncio`, `pytest-cov`
- **Qualidade/segurança**: ruff (lint), bandit (SAST), pip-audit (SCA), SonarQube

## Funcionalidades principais

| Módulo | O que faz |
|---|---|
| Clientes | CRUD, identificação por CPF/CNPJ (Value Object validado na criação) |
| Veículos | CRUD, placa validada, vinculado a um cliente |
| Serviços | CRUD do catálogo de serviços oferecidos |
| Peças | CRUD com controle de estoque (baixa/reposição atômica) |
| Ordens de Serviço | Criação com orçamento automático, máquina de estados completa, notificação de orçamento por e-mail, consulta pública de status, relatório de tempo médio de execução |
| Usuários/Auth | Login JWT, RBAC por perfil (`ADMIN`/`ATENDENTE`/`MECANICO`) |

## Requisitos

Para rodar via Docker (recomendado):

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose

Para rodar localmente sem Docker:

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Um Postgres acessível (pode ser só o banco via `docker compose up -d db`)

## Dados iniciais para uso

Copie o `.env.example` para `.env` (ver [Configuração do `.env`](#configuração-do-env)
abaixo), depois:

**Via Docker Compose:**

```bash
docker compose up --build
docker compose exec api uv run python -m scripts.seed_admin
```

**Local, sem Docker:**

```bash
uv sync
uv run alembic upgrade head
uv run python -m scripts.seed_admin
uv run uvicorn app.main:app --reload --port 8000
```

(`uv run fastapi dev app/main.py` também funciona, mas o `fastapi-cli` quebra em
consoles Windows sem UTF-8 ativo por causa de um emoji na saída — `uvicorn` direto evita
esse problema.)

O `seed_admin` cria o usuário administrador inicial com as credenciais definidas em
`SEED_ADMIN_EMAIL`/`SEED_ADMIN_SENHA` no `.env` (é idempotente — rodar de novo não
duplica o usuário). Use essas credenciais em `POST /api/v1/auth/login` para obter o
token JWT e acessar as rotas administrativas.

## Configuração do `.env`

Todas as variáveis do `.env.example` são obrigatórias — a aplicação não sobe se alguma
faltar (ver `app/shared/settings.py`), inclusive em ambiente local:

```bash
cp .env.example .env
```

Pontos de atenção:

- `DATABASE_URL` / `POSTGRES_*`: credenciais do Postgres principal (dev).
- `TEST_POSTGRES_*`: só para o Postgres efêmero dos testes de integração
  (`docker-compose.test.yml`), nunca guarda dado real.
- `JWT_SECRET_KEY`: assina os tokens — troque por uma chave própria fora de avaliação
  local (`python -c "import secrets; print(secrets.token_urlsafe(32))"`).
- `NOTIFICACAO_BACKEND`: `log` (padrão, só registra em log) ou `smtp` (envia e-mail de
  verdade — exige preencher todas as variáveis `SMTP_*`).

## Documentação da API

Com a aplicação rodando:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testes

```bash
uv run pytest                    # unitários (domain + application) - não precisam de banco
```

Os testes de integração (`tests/integration/`) sobem contra um Postgres efêmero, separado do
banco de desenvolvimento (porta 5433). Suba o container antes de rodá-los:

```bash
docker compose -f docker-compose.test.yml up -d
uv run pytest tests/integration
docker compose -f docker-compose.test.yml down
```

Cobertura (`uv run pytest --cov=app --cov-report=term-missing`), rodada mais recente:

<details>
<summary>Ver relatório completo</summary>

```
Camada          Statements   Miss   Cobertura
domain          341          0      100.0%
application     756          0      100.0%
infrastructure  416          7      98.3%
presentation    702          34     95.2%
shared          34           0      100.0%
------------------------------------------
TOTAL           2278         42     98%

267 passed, 3 warnings in 15.62s
```

</details>

Domínio e aplicação (onde vive a regra de negócio) em 100% — as lacunas restantes são
principalmente ramos de tratamento de exceção em controllers e trechos de bootstrap de
infraestrutura, cobertos indiretamente pelos testes de integração.

## Segurança

Scan de vulnerabilidades (SAST + SCA), rodado a cada release:

```bash
uv run bandit -r app scripts   # análise estática do código
uv run pip-audit               # CVEs conhecidas nas dependências
```

Resultado mais recente e cobertura por categoria do OWASP Top 10 em
[docs/relatorio-vulnerabilidades.md](docs/relatorio-vulnerabilidades.md).

## Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/leonardo-abe">
        <img src="https://github.com/leonardo-abe.png" width="100px;" alt="Foto de Leonardo Tadanory Abe no GitHub"/>
        <br />
        <sub><b>Leonardo Tadanory Abe</b></sub>
      </a>
    </td>
  </tr>
</table>
