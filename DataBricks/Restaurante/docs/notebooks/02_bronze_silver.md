# Notebook: Bronze-Silver.py

**Propósito:** Limpar, padronizar e enriquecer os dados brutos da camada Bronze.

## Ações Executadas

1.  **Leitura da Camada Bronze**
    * O notebook lê as tabelas `bronze.*` (ex: `bronze.franquias`) em DataFrames Spark.

2.  **Transformações de Qualidade (Helpers)**
    * Uma função `_apply_name_rules` é usada para padronizar todos os nomes de colunas.
        * Converte para maiúsculas (ex: `nome_franquia` -> `NOME_FRANQUIA`).
        * Padroniza prefixos de ID (ex: `id_franquia` -> `SK_FRANQUIA`), preparando os dados para a modelagem na camada Gold.
    * Metadados de auditoria da Bronze (`DATA_HORA_BRONZE`) são removidos.
    * Novos metadados de auditoria da Silver (`FONTE_BRONZE`, `DATA_PROCESSAMENTO_SILVER`) são adicionados.

3.  **Salvar na Camada Silver**
    * Os DataFrames limpos e padronizados são salvos como tabelas Delta no schema `silver`.
    * A opção `option("overwriteSchema", "true")` é usada para permitir a evolução do schema (ex: adição de novas colunas de auditoria) sem falhar.