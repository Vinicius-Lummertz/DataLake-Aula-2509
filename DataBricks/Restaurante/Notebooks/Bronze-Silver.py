# Databricks notebook source
# MAGIC %md
# MAGIC ## Pipeline Restaurante: Bronze para Silver
# MAGIC 
# MAGIC Aplicando limpezas, padronizações e transformações nos dados da camada Bronze e salvando na Silver.

# COMMAND ----------

from pyspark.sql import functions as F

# ---------- Funções Auxiliares (Helpers) ----------
def _apply_name_rules(colname: str) -> str:
    """Regras de renomeação: maiúsculas e padronização de prefixos."""
    n = colname.upper()
    n = n.replace("ID_", "SK_") # Preparando para a Gold
    return n

def _safe_drop(df, cols):
    """Remove colunas somente se existirem no DataFrame."""
    existing = set(df.columns)
    to_drop = [c for c in cols if c in existing]
    return df.drop(*to_drop) if to_drop else df

# ---------- Função Principal de Transformação ----------
def processar_para_silver(src_table: str, dest_table: str):
    """
    Lê uma tabela da camada Bronze, aplica as regras de qualidade e salva na camada Silver.
    - src_table: Nome da tabela de origem (ex: 'franquias')
    - dest_table: Nome da tabela de destino (ex: 'franquias_silver')
    """
    src_fqn = f"bronze.{src_table}"
    dest_fqn = f"silver.{dest_table}"
    
    df = spark.read.format("delta").table(src_fqn)

    # Renomeia todas as colunas
    new_cols = [_apply_name_rules(c) for c in df.columns]
    df = df.toDF(*new_cols)

    # Remove colunas antigas de metadados
    df = _safe_drop(df, ["DATA_HORA_BRONZE", "NOME_ARQUIVO"])

    # Adiciona novas colunas de auditoria para a camada Silver
    df = (df
          .withColumn("FONTE_BRONZE", F.lit(src_fqn))
          .withColumn("DATA_PROCESSAMENTO_SILVER", F.current_timestamp())
         )

    # Salva como Tabela Gerenciada (Managed Table) na Silver
    (df.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true") # Permite evoluir o schema
       .saveAsTable(dest_fqn))
    
    print(f"Tabela '{src_fqn}' processada e salva como '{dest_fqn}'.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Executando o Processamento para Todas as Tabelas

# COMMAND ----------

tabelas_bronze = ["franquias", "profissionais", "ingredientes", "cardapio", "vendas"]

for tabela in tabelas_bronze:
    processar_para_silver(tabela, tabela) # Mantém o mesmo nome de tabela na Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver;