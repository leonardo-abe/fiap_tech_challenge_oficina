# fiap_tech_challenge_oficina
Backend de uma oficina de medio porte.

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

## Segurança

Scan de vulnerabilidades (SAST + SCA), rodado a cada release:

```bash
uv run bandit -r app scripts   # análise estática do código
uv run pip-audit               # CVEs conhecidas nas dependências
```

Resultado mais recente e cobertura por categoria do OWASP Top 10 em
[docs/relatorio-vulnerabilidades.md](docs/relatorio-vulnerabilidades.md).
