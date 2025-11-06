# Notebook: Landing-Bronze.py

**Propósito:** Ingestar os dados brutos (Extract/Load) do Volume e salvá-los na camada Bronze.

## Ações Executadas

1.  **Simulação de Ingestão**
    * Para tornar o projeto autocontido, este notebook primeiro **gera os dados de exemplo** (vendas, franquias, profissionais, etc.).
    * Ele usa `dbutils.fs.put()` para salvar esses dados como arquivos CSV no Volume `workspace.landing.dados`, que foi criado pelo notebook `Setup.py`.

2.  **Leitura dos Dados Brutos**
    * Os arquivos CSV são lidos do Volume usando `spark.read.csv()`.
    * As opções `header=True` e `inferSchema=True` são usadas para carregar os dados corretamente.

3.  **Adição de Metadados (Auditoria)**
    * Duas colunas de auditoria são adicionadas aos DataFrames:
        * `data_hora_bronze`: Marca o timestamp da ingestão (`current_timestamp()`).
        * `fonte_dados`: Identifica a origem dos dados (ex: "Volume_Landing_CSV").

4.  **Salvar na Camada Bronze**
    * Os DataFrames enriquecidos são salvos como tabelas Delta no schema `bronze` (ex: `bronze.vendas`).
    * `mode("overwrite")` é usado para permitir que o pipeline seja re-executado.