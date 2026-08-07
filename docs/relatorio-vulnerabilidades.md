# Relatório de Vulnerabilidades

**Data:** 2026-08-07
**Ferramentas:** [bandit](https://bandit.readthedocs.io/) 1.9.4 (SAST) · [pip-audit](https://pypi.org/project/pip-audit/) 2.10.1 (SCA) · [SonarQube](https://www.sonarsource.com/products/sonarqube/) Community Edition (SAST/hotspots, self-hosted)
**Ambiente:** Python 3.12.8

## Como reproduzir

```bash
uv run bandit -r app scripts
uv run pip-audit
```

SonarQube foi rodado localmente via Docker, com o repositório integrado diretamente
(sem necessidade de CI, já que o projeto não usa pipeline).

## Resultados

### SAST — bandit (análise estática do código)

```
Total lines of code: 3320
Total issues (by severity): Undefined: 0, Low: 0, Medium: 0, High: 0
```

Nenhum achado em `app/` e `scripts/`.

### SCA — pip-audit (dependências)

```
No known vulnerabilities found
```

Nenhuma vulnerabilidade conhecida nas dependências instaladas (produção + dev).

### SAST — SonarQube (Security Rating por arquivo)

A primeira rodada apontou Security Rating `E` em 3 arquivos e `D` em 1 (os demais 353
componentes analisados ficaram em `A`). Cada um foi investigado individualmente:

| Arquivo | Rating inicial | Natureza | Ação |
|---|---|---|---|
| `Dockerfile` | D | Real: container rodava como root (sem `USER`) | **Corrigido** - usuário `appuser` não-root criado e usado a partir do fim do build |
| `docker-compose.yml` | E | Real, risco baixo: credenciais do Postgres hardcoded no arquivo versionado | **Corrigido** - movidas para variáveis de ambiente (`${POSTGRES_USER:-oficina}` etc.), com fallback para não quebrar o `docker-compose up` de quem não criou um `.env` |
| `app/application/usuario/use_cases/autenticar_usuario.py` | E | Falso positivo: `_HASH_SEM_CORRESPONDENCIA` é um hash bcrypt fixo *de propósito* (mitigação de timing attack no login, nunca corresponde a senha real) | Security Hotspot marcado como **Safe** no SonarQube, com a justificativa acima |
| `app/shared/settings.py` | E | Falso positivo / risco documentado: `jwt_secret_key` e `seed_admin_senha` são *defaults* de ambiente local, já documentados no `.env.example` como "troque em produção" | Security Hotspots marcados como **Safe** no SonarQube, com a mesma justificativa |

Diferença importante em relação a bandit/pip-audit: os achados de credencial hardcoded do
SonarQube são **Security Hotspots**, não "Issues" - por design, o SonarQube exige revisão
humana explícita (status Safe/Fixed/Acknowledged na própria interface) em vez de permitir
suprimir via comentário no código. Isso é intencional: força alguém a efetivamente olhar
cada caso antes de descartá-lo.

## Cobertura por categoria do OWASP Top 10 (2021)

Como os scanners não encontraram achados, esta seção documenta como cada categoria do
OWASP Top 10 é tratada pela arquitetura atual — é isso que embasa a confiança no
resultado "limpo" acima, e também onde ficam registradas as lacunas conhecidas.

| # | Categoria | Situação | Como é tratada |
|---|---|---|---|
| A01 | Broken Access Control | Mitigado | RBAC por perfil (`ADMIN`/`ATENDENTE`/`MECANICO`) via dependency `require_roles`, aplicado por rota/roteador conforme a tabela de permissões do desafio; perfil embutido como claim no JWT, não em dado que o cliente possa manipular sem invalidar a assinatura. |
| A02 | Cryptographic Failures | Mitigado | Senha de usuário nunca fica em texto puro (hash `bcrypt`); JWT assinado com `HS256` via chave em variável de ambiente (`JWT_SECRET_KEY`); valores monetários usam `Decimal`, nunca `float`, evitando erro de arredondamento em dado sensível. Corrigido nesta rodada: o *default* de desenvolvimento de `jwt_secret_key` tinha 23 bytes, abaixo do mínimo de 32 recomendado pela RFC 7518 §3.2 para HS256 — alertado pelo próprio `PyJWT` (`InsecureKeyLengthWarning`) durante a suíte de testes. Ajustado para 42 bytes (continua um placeholder, sempre sobrescrito por env var em produção). |
| A03 | Injection | Mitigado | Toda persistência via SQLAlchemy ORM parametrizado — nenhuma concatenação de SQL bruta no projeto. Entradas validadas na borda por schemas Pydantic antes de chegar à aplicação; `Documento`/`Placa`/`Money` validam formato na própria construção do Value Object. |
| A04 | Insecure Design | Mitigado | Clean Architecture com regra de dependência única (domínio não conhece framework); invariantes de negócio garantidas por Value Objects e pela máquina de estados explícita de `OrdemServico` (transição inválida é rejeitada no domínio, não checada "por fora"). |
| A05 | Security Misconfiguration | Mitigado | Configuração via `pydantic-settings` + `.env` (fora do controle de versão, ver `.gitignore`); exceções de domínio são mapeadas para respostas HTTP genéricas pelos exception handlers — nenhum stack trace ou detalhe interno é exposto ao cliente. |
| A06 | Vulnerable and Outdated Components | Verificado | `pip-audit` sem vulnerabilidades conhecidas na data acima; `uv.lock` fixa versões exatas. Precisa ser reexecutado periodicamente, já que novas CVEs são publicadas independentemente de mudança no código. |
| A07 | Identification and Authentication Failures | Mitigado | Login por JWT com expiração (`JWT_EXPIRACAO_MINUTOS`); verificação de senha sempre executa o `bcrypt.checkpw` contra um hash constante quando o e-mail não existe, para não vazar por tempo de resposta se um e-mail está cadastrado; usuário inativo é bloqueado no login mesmo com senha correta. |
| A08 | Software and Data Integrity Failures | Mitigado | Nenhum uso de `pickle`/`eval`/deserialização insegura sobre dado não confiável; `uv.lock` garante builds reprodutíveis (mesmas versões/hashes). |
| A09 | Security Logging and Monitoring Failures | Lacuna conhecida | Não há logging estruturado de eventos de segurança (tentativas de login falhas, mudanças de permissão). Fora do escopo do MVP; registrado aqui como melhoria futura. |
| A10 | Server-Side Request Forgery (SSRF) | Não aplicável | A API não faz requisições HTTP de saída a partir de entrada do usuário. |

## Achados corrigidos nesta rodada

- `app/shared/settings.py`: *default* de `jwt_secret_key` alongado de 23 para 42 bytes (RFC 7518 §3.2), eliminando o `InsecureKeyLengthWarning` observado na suíte de testes.
- `Dockerfile`: container passou a rodar como usuário não-root (`appuser`) a partir do fim do build, em vez de root.
- `docker-compose.yml` / `docker-compose.test.yml`: credenciais do Postgres movidas de literal hardcoded para variável de ambiente com fallback (`${POSTGRES_USER:-oficina}` etc.).

## Limitações desta análise

- `bandit`/`pip-audit` são ferramentas automatizadas — não substituem revisão manual nem pentest.
- `pip-audit` audita o ambiente instalado no momento da execução; deve ser reexecutado a cada atualização de dependência e periodicamente mesmo sem mudança de código.
