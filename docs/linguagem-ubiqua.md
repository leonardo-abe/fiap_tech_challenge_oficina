# Linguagem Ubíqua

Termos do negócio da oficina e onde cada um está representado no código — nomes de
classes e métodos espelham este vocabulário, não termos técnicos genéricos.

| Termo de negócio | Representação no código | Significado |
|---|---|---|
| Ordem de Serviço (OS) | `OrdemServico` (`app/domain/ordem_servico/entities/`) — aggregate root | Registro central do atendimento: um veículo, um cliente, os serviços/peças envolvidos e o status atual |
| Orçamento | `Orcamento` (Value Object) | Soma de `itens_servico` + `itens_peca` de uma OS — sempre calculado a partir dos itens, nunca digitado manualmente |
| Diagnóstico | Status `EM_DIAGNOSTICO`, ação `iniciar_diagnostico` | Etapa em que o mecânico avalia o veículo antes de definir os reparos |
| Aprovação do orçamento | Status `AGUARDANDO_APROVACAO`, ações `aprovar_orcamento`/`reprovar_orcamento` | Decisão sobre executar ou não os reparos propostos, comunicada ao cliente por e-mail |
| Execução | Status `EM_EXECUCAO` | Serviços/reparos sendo realizados; marca `execucao_iniciada_em` |
| Finalização | Status `FINALIZADA` | Serviços concluídos; marca `finalizada_em`, usado no relatório de tempo médio |
| Entrega | Status `ENTREGUE`, ação `entregar` | Veículo devolvido ao cliente — status terminal do fluxo normal |
| Reprovação / Cancelamento | Status `REPROVADA` / `CANCELADA` | Encerramentos alternativos: cliente não aprovou o orçamento, ou a OS foi cancelada antes disso |
| Cliente | `Cliente` (entidade) | Pessoa física ou jurídica dona do veículo, identificada de forma única por `Documento` |
| Documento | `Documento` (Value Object) | CPF ou CNPJ validado (dígito verificador) na própria construção |
| Veículo | `Veiculo` (entidade) | Carro/moto do cliente, identificado de forma única por `Placa` |
| Placa | `Placa` (Value Object) | Identificador único do veículo, formato validado na construção |
| Serviço | `Servico` (entidade) | Item do catálogo de mão de obra oferecido pela oficina (ex.: troca de óleo, alinhamento) |
| Peça / Insumo | `Peca` (entidade) | Item físico consumido na execução, com `quantidade_disponivel` controlada |
| Item de Serviço / Item de Peça | `ItemServico` / `ItemPeca` (entidades filhas da OS) | "Fotografia" do serviço/peça no momento em que entrou na OS — nome e valor congelados, não mudam se o catálogo for atualizado depois |
| Dinheiro | `Money` (Value Object) | Valor monetário em `Decimal`, sempre arredondado a 2 casas, nunca negativo |
| Usuário | `Usuario` (entidade) | Funcionário da oficina com acesso ao sistema |
| Perfil | `Perfil` (enum: `ADMIN`/`ATENDENTE`/`MECANICO`) | Papel do usuário — define quais ações ele pode executar (RBAC) |
| Status da OS | `StatusOS` (enum) | Estado atual da ordem de serviço na máquina de estados do domínio |
