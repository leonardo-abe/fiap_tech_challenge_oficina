# Escolha do banco de dados

O desafio permite livre escolha de banco, exigindo apenas justificar a preferência.
Este projeto usa **PostgreSQL 16**, acessado via SQLAlchemy 2.0 assíncrono (`asyncpg`).

## Motivos

- **Domínio fortemente relacional**: cliente → veículo → OS → itens de serviço/peça, com
  integridade referencial real entre eles (uma OS não existe sem cliente e veículo
  válidos, um item de peça não existe sem uma peça cadastrada). Um banco relacional
  modela isso nativamente; um documento/NoSQL exigiria reconstruir essas garantias na
  aplicação.
- **Concorrência real na baixa de estoque**: duas Ordens de Serviço podem decrementar o
  estoque da mesma peça ao mesmo tempo. A correção depende de `UPDATE` atômico
  condicional (`WHERE quantidade_disponivel >= quantidade`) rodando dentro de uma
  transação ACID — garantia que o Postgres oferece nativamente, sem coordenação extra na
  aplicação.
- **Precisão monetária**: valores usam `Decimal` de ponta a ponta (nunca `float`,
  incluindo no domínio, ver `Money`); o tipo `NUMERIC` do Postgres preserva essa precisão
  sem conversão, diferente de bancos cujo driver ou tipo nativo força passagem por
  `float`/`double`.
- **Custo e maturidade**: gratuito, sem serviço gerenciado obrigatório, com driver
  assíncrono de primeira classe (`asyncpg`) e imagem oficial (`postgres:16-alpine`) — sobe
  localmente com um `docker compose up`, sem licenciamento.

## Alternativas consideradas e descartadas

- **SQLite**: suficiente para os testes unitários não precisarem de banco real, mas não
  seria adequado como banco principal — não oferece as garantias de concorrência
  (`UPDATE` condicional sob load concorrente real, múltiplos workers) que a baixa de
  estoque exige.
- **MongoDB / documento**: o domínio não tem a forma de "documentos semi-estruturados
  independentes" — é o oposto, entidades fortemente conectadas com integridade
  referencial exigida entre elas. Modelar isso em um documento único por OS
  (duplicando cliente/veículo/peça embutidos) traria os problemas clássicos de
  denormalização (dado desatualizado, sem transação cross-documento nativa para a baixa
  de estoque).
