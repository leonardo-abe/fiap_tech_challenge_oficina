from pathlib import Path

from fpdf import FPDF

_OWASP = [
    (
        "A01 - Broken Access Control",
        "Mitigado",
        "RBAC por perfil (ADMIN/ATENDENTE/MECANICO) via dependency require_roles, aplicado "
        "por rota/roteador conforme a tabela de permissoes do desafio; perfil embutido como "
        "claim no JWT, nao em dado que o cliente possa manipular sem invalidar a assinatura.",
    ),
    (
        "A02 - Cryptographic Failures",
        "Mitigado",
        "Senha de usuario nunca fica em texto puro (hash bcrypt); JWT assinado com HS256 via "
        "chave em variavel de ambiente (JWT_SECRET_KEY); valores monetarios usam Decimal, "
        "nunca float. Corrigido nesta rodada: o default de desenvolvimento de jwt_secret_key "
        "tinha 23 bytes, abaixo do minimo de 32 recomendado pela RFC 7518 par. 3.2 para "
        "HS256 - alertado pelo proprio PyJWT (InsecureKeyLengthWarning) durante a suite de "
        "testes. Ajustado para 42 bytes (continua um placeholder, sempre sobrescrito por env "
        "var em producao).",
    ),
    (
        "A03 - Injection",
        "Mitigado",
        "Toda persistencia via SQLAlchemy ORM parametrizado - nenhuma concatenacao de SQL "
        "bruta no projeto. Entradas validadas na borda por schemas Pydantic antes de chegar "
        "a aplicacao; Documento/Placa/Money validam formato na propria construcao do Value "
        "Object.",
    ),
    (
        "A04 - Insecure Design",
        "Mitigado",
        "Clean Architecture com regra de dependencia unica (dominio nao conhece framework); "
        "invariantes de negocio garantidas por Value Objects e pela maquina de estados "
        "explicita de OrdemServico (transicao invalida e rejeitada no dominio, nao checada "
        "por fora).",
    ),
    (
        "A05 - Security Misconfiguration",
        "Mitigado",
        "Configuracao via pydantic-settings + .env (fora do controle de versao, ver "
        ".gitignore); excecoes de dominio sao mapeadas para respostas HTTP genericas pelos "
        "exception handlers - nenhum stack trace ou detalhe interno e exposto ao cliente.",
    ),
    (
        "A06 - Vulnerable and Outdated Components",
        "Verificado",
        "pip-audit sem vulnerabilidades conhecidas na data deste relatorio; uv.lock fixa "
        "versoes exatas. Precisa ser reexecutado periodicamente, ja que novas CVEs sao "
        "publicadas independentemente de mudanca no codigo.",
    ),
    (
        "A07 - Identification and Authentication Failures",
        "Mitigado",
        "Login por JWT com expiracao (JWT_EXPIRACAO_MINUTOS); verificacao de senha sempre "
        "executa o bcrypt.checkpw contra um hash constante quando o e-mail nao existe, para "
        "nao vazar por tempo de resposta se um e-mail esta cadastrado; usuario inativo e "
        "bloqueado no login mesmo com senha correta.",
    ),
    (
        "A08 - Software and Data Integrity Failures",
        "Mitigado",
        "Nenhum uso de pickle/eval/deserializacao insegura sobre dado nao confiavel; uv.lock "
        "garante builds reprodutiveis (mesmas versoes/hashes).",
    ),
    (
        "A09 - Security Logging and Monitoring Failures",
        "Lacuna conhecida",
        "Nao ha logging estruturado de eventos de seguranca (tentativas de login falhas, "
        "mudancas de permissao). Fora do escopo do MVP, registrado aqui como melhoria "
        "futura.",
    ),
    (
        "A10 - Server-Side Request Forgery (SSRF)",
        "Nao aplicavel",
        "A API nao faz requisicoes HTTP de saida a partir de entrada do usuario.",
    ),
]


class _RelatorioPDF(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Relatorio de Vulnerabilidades - Oficina Mecanica API")
        self.ln(10)


def _bloco(pdf, texto, size=10, style="", color=(40, 40, 40), altura=5.5, espaco_depois=1):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, altura, texto, new_x="LMARGIN", new_y="NEXT")
    if espaco_depois:
        pdf.ln(espaco_depois)


def _h1(pdf, texto):
    _bloco(pdf, texto, size=16, style="B", color=(20, 20, 20), altura=9, espaco_depois=2)


def _h2(pdf, texto):
    pdf.ln(2)
    _bloco(pdf, texto, size=12, style="B", color=(20, 20, 20), altura=7, espaco_depois=1)


def _h3(pdf, texto):
    _bloco(pdf, texto, size=10.5, style="B", color=(20, 20, 20), altura=6, espaco_depois=0)


def _paragrafo(pdf, texto):
    _bloco(pdf, texto, size=10, style="", color=(40, 40, 40), altura=5.5, espaco_depois=1)


def _codigo(pdf, texto):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(30, 30, 30)
    pdf.set_fill_color(240, 240, 240)
    pdf.multi_cell(0, 5, texto, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def gerar_relatorio_pdf(
    destino: Path, data: str, versao_bandit: str, versao_pip_audit: str
) -> None:
    pdf = _RelatorioPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)
    pdf.add_page()

    _h1(pdf, "Relatorio de Vulnerabilidades")
    _paragrafo(pdf, "Sistema Integrado de Atendimento e Execucao de Servicos - Oficina Mecanica")

    _bloco(pdf, f"Data: {data}", color=(90, 90, 90))
    _bloco(
        pdf,
        f"Ferramentas: bandit {versao_bandit} (SAST), pip-audit {versao_pip_audit} (SCA) e "
        "SonarQube Community Edition (SAST/hotspots, self-hosted)",
        color=(90, 90, 90),
    )
    _bloco(pdf, "Ambiente: Python 3.12.8", color=(90, 90, 90))
    pdf.ln(2)

    _h2(pdf, "Como reproduzir")
    _codigo(pdf, "uv run bandit -r app scripts\nuv run pip-audit")

    _h2(pdf, "Resultados")

    _h3(pdf, "SAST - bandit (analise estatica do codigo)")
    _codigo(
        pdf,
        "Total lines of code: 3320\n"
        "Total issues (by severity): Undefined: 0, Low: 0, Medium: 0, High: 0",
    )
    _paragrafo(pdf, "Nenhum achado em app/ e scripts/.")

    _h3(pdf, "SCA - pip-audit (dependencias)")
    _codigo(pdf, "No known vulnerabilities found")
    _paragrafo(
        pdf, "Nenhuma vulnerabilidade conhecida nas dependencias instaladas (producao + dev)."
    )

    _h3(pdf, "SAST - SonarQube (Security Rating por arquivo)")
    _paragrafo(
        pdf,
        "Primeira rodada apontou Security Rating E em 3 arquivos e D em 1 (os demais 353 "
        "componentes analisados ficaram em A). Cada um foi investigado individualmente:",
    )
    _paragrafo(
        pdf,
        "- Dockerfile (D): real - container rodava como root. Corrigido: usuario appuser "
        "nao-root a partir do fim do build.\n"
        "- docker-compose.yml (E): real, risco baixo - credenciais do Postgres hardcoded no "
        "arquivo versionado. Corrigido: movidas para variavel de ambiente com fallback.\n"
        "- autenticar_usuario.py (E): falso positivo - hash bcrypt fixo de proposito "
        "(mitigacao de timing attack no login). Security Hotspot marcado Safe no SonarQube.\n"
        "- settings.py (E): falso positivo / risco documentado - jwt_secret_key e "
        "seed_admin_senha sao defaults de ambiente local, ja documentados no .env.example. "
        "Security Hotspots marcados Safe no SonarQube.",
    )
    _paragrafo(
        pdf,
        "Diferenca em relacao a bandit/pip-audit: achados de credencial hardcoded do "
        "SonarQube sao Security Hotspots, nao Issues - por design, exigem revisao humana "
        "explicita (status Safe/Fixed/Acknowledged na propria interface) em vez de "
        "supressao via comentario no codigo.",
    )

    _h3(pdf, "SonarQube Cloud (integracao direta com o GitHub) - Quality Gate")
    _paragrafo(
        pdf,
        "Alem da rodada local (self-hosted, acima), o repositorio foi integrado "
        "diretamente ao SonarQube Cloud via GitHub. Snapshot do dashboard (Overall "
        "Code), apos as correcoes desta rodada:",
    )
    _paragrafo(
        pdf,
        "- Quality Gate (Sonar way): Passed\n"
        "- Security: E - 6 issues em aberto\n"
        "- Reliability: A - 0 issues em aberto\n"
        "- Maintainability: A - 33 issues em aberto (code smells)\n"
        "- Duplications: 0.0%\n"
        "- Coverage: nao configurada nesta integracao (exige um passo extra de setup no "
        "SonarQube Cloud)\n"
        "- Security Hotspots (metrica legada, sendo descontinuada): 0",
    )
    _paragrafo(
        pdf,
        "O Quality Gate padrao (Sonar way) avalia principalmente metricas de New Code, "
        "nao de Overall Code - por isso aparece como Passed mesmo com o rating de "
        "Security em E no codigo ja existente. Os 6 issues de Security e os 33 de "
        "Maintainability ainda nao foram triados individualmente item a item (fica para "
        "uma proxima rodada). A cobertura de testes real do projeto (100% em "
        "domain/application, 98% em app/ inteiro, ver README.md) nao e reportada "
        "automaticamente para o SonarQube Cloud sem esse passo extra de integracao.",
    )

    _h2(pdf, "Cobertura por categoria do OWASP Top 10 (2021)")
    _paragrafo(
        pdf,
        "Como os scanners nao encontraram achados, esta secao documenta como cada categoria "
        "do OWASP Top 10 e tratada pela arquitetura atual - e isso que embasa a confianca no "
        'resultado "limpo" acima, e tambem onde ficam registradas as lacunas conhecidas.',
    )

    for titulo, situacao, texto in _OWASP:
        _h3(pdf, f"{titulo}  [{situacao}]")
        _paragrafo(pdf, texto)

    _h2(pdf, "Achados corrigidos nesta rodada")
    _paragrafo(
        pdf,
        "- app/shared/settings.py: default de jwt_secret_key alongado de 23 para 42 bytes "
        "(RFC 7518 par. 3.2), eliminando o InsecureKeyLengthWarning observado na suite de "
        "testes.\n"
        "- Dockerfile: container passou a rodar como usuario nao-root (appuser) a partir do "
        "fim do build, em vez de root.\n"
        "- docker-compose.yml / docker-compose.test.yml: credenciais do Postgres movidas de "
        "literal hardcoded para variavel de ambiente com fallback.",
    )

    _h2(pdf, "Limitacoes desta analise")
    _paragrafo(
        pdf,
        "- bandit/pip-audit sao ferramentas automatizadas - nao substituem revisao manual "
        "nem pentest.",
    )
    _paragrafo(
        pdf,
        "- pip-audit audita o ambiente instalado no momento da execucao; deve ser "
        "reexecutado a cada atualizacao de dependencia e periodicamente mesmo sem mudanca "
        "de codigo.",
    )

    pdf.output(str(destino))


if __name__ == "__main__":
    _destino = Path(__file__).resolve().parent.parent / "docs" / "relatorio-vulnerabilidades.pdf"
    gerar_relatorio_pdf(
        destino=_destino, data="2026-08-07", versao_bandit="1.9.4", versao_pip_audit="2.10.1"
    )
    print(f"PDF gerado em {_destino}")
