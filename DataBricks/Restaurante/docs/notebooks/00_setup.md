# Notebook: Setup.py

**Propósito:** Preparar e limpar o ambiente do Databricks para a execução do pipeline.

Este notebook é o ponto de partida e garante que o pipeline seja idempotente (possa ser executado várias vezes do zero).

## Ações Executadas

1.  **Limpeza Total (Cleanup)**
    * Executa `DROP SCHEMA IF EXISTS ... CASCADE` para os schemas `landing`, `bronze`, `silver`, e `gold`.
    * O uso de `CASCADE` garante que todas as tabelas, views e volumes dentro desses schemas sejam removidos primeiro.

2.  **Criação dos Schemas**
    * Cria os schemas `landing`, `bronze`, `silver`, e `gold` no catálogo `workspace`.

3.  **Criação do Volume**
    * Cria o Volume `workspace.landing.dados`. Este volume é usado como a "Landing Zone" para receber os arquivos CSV brutos.