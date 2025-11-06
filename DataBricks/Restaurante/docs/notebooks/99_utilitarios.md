# Notebooks: Utilitários

## `ShowTables.py`

**Propósito:** Um "dashboard" simples para verificar os resultados finais do pipeline.

Este notebook não faz parte do processo de ELT, mas é usado para validar os dados na camada Gold.

* Executa `SELECT *` em todas as tabelas do schema `gold`:
    * `gold.dim_franquia`
    * `gold.dim_profissional`
    * `gold.dim_cardapio`
    * `gold.dim_tempo`
    * `gold.fato_vendas`

## `Cleanup.py`

**Propósito:** Limpar completamente todos os artefatos criados pelo pipeline.

Este notebook pode ser executado a qualquer momento para "resetar" o ambiente.

* Executa `DROP SCHEMA IF EXISTS ... CASCADE` nos schemas `landing`, `bronze`, `silver`, e `gold`.