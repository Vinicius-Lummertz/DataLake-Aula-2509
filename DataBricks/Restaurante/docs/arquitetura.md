# Arquitetura do Pipeline

O pipeline segue a arquitetura Medalhão, dividida em três camadas:

## Camada Bronze
- **Objetivo:** Ingestão de dados brutos.
- **Formato:** Tabelas Delta.
- **Processo:** Leitura dos arquivos CSV e adição de metadados de controle.

## Camada Silver
- **Objetivo:** Dados limpos e padronizados.
- **Formato:** Tabelas Delta.
- **Processo:** Renomeação de colunas, tipagem de dados e validações de qualidade.

## Camada Gold
- **Objetivo:** Modelo otimizado para análise (BI).
- **Formato:** Star Schema com tabelas Delta.
- **Processo:** Criação de tabelas dimensão e fato a partir da camada Silver.