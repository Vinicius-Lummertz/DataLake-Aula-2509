# Modelo de Dados (Camada Gold)

A camada Gold é modelada como um **Star Schema** para otimizar consultas analíticas e facilitar o consumo por ferramentas de BI.

O modelo consiste em uma tabela Fato central (`fato_vendas`) e quatro tabelas de Dimensão.

## Tabela Fato

### `gold.fato_vendas`
Armazena as métricas de negócio (quantidades e valores) de cada transação.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `SK_VENDA` | BIGINT | Chave primária da tabela de fatos (IDENTITY) |
| `FK_FRANQUIA` | BIGINT | Chave estrangeira para `dim_franquia` |
| `FK_PROFISSIONAL` | BIGINT | Chave estrangeira para `dim_profissional` |
| `FK_PRATO` | BIGINT | Chave estrangeira para `dim_cardapio` |
| `FK_TEMPO` | INT | Chave estrangeira para `dim_tempo` (no formato YYYYMMDD) |
| `QUANTIDADE` | INT | Quantidade de itens vendidos na transação |
| `VALOR_TOTAL` | DECIMAL(10, 2) | Valor total da transação |

## Tabelas de Dimensão

### `gold.dim_franquia`
Dimensão que armazena os detalhes das filiais.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `SK_FRANQUIA` | BIGINT | Chave primária (Surrogate Key, vinda da Bronze) |
| `NOME_FRANQUIA` | STRING | Nome da filial |
| `CIDADE` | STRING | Cidade da filial |
| `ESTADO` | STRING | Estado (UF) da filial |

### `gold.dim_profissional`
Dimensão com a lista de funcionários.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `SK_PROFISSIONAL` | BIGINT | Chave primária (Surrogate Key, vinda da Bronze) |
| `NOME_PROFISSIONAL` | STRING | Nome do funcionário |
| `CARGO` | STRING | Cargo do funcionário |

### `gold.dim_cardapio`
Dimensão com os itens do menu.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `SK_PRATO` | BIGINT | Chave primária (Surrogate Key, vinda da Bronze) |
| `NOME_PRATO` | STRING | Nome do item/prato |
| `PRECO` | DECIMAL(10, 2) | Preço unitário do prato |
| `CATEGORIA` | STRING | Categoria (ex: Lanche, Bebida) |

### `gold.dim_tempo`
Dimensão de data gerada para permitir análises temporais (diárias, mensais, etc.).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `SK_TEMPO` | INT | Chave primária no formato YYYYMMDD |
| `DATA` | DATE | Data completa (ex: 2025-01-01) |
| `ANO` | INT | Ano (ex: 2025) |
| `MES` | INT | Mês (ex: 1) |
| `DIA` | INT | Dia (ex: 1) |
| `DIA_DA_SEMANA` | INT | Dia da semana (ex: 1 = Domingo) |