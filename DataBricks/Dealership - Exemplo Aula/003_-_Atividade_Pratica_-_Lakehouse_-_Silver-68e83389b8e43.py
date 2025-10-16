# Databricks notebook source
# MAGIC %md
# MAGIC ## df = spark.read.format('delta').load(f"schema.tabela")
# MAGIC
# MAGIC Gera um dataframe para cada tabela delta de bronze.
# MAGIC

# COMMAND ----------

df_apolice   = spark.read.format("delta").table("bronze.apolice")
df_carro     = spark.read.format("delta").table("bronze.carro")
df_cliente   = spark.read.format("delta").table("bronze.cliente")
df_endereco  = spark.read.format("delta").table("bronze.endereco")
df_estado    = spark.read.format("delta").table("bronze.estado")
df_marca     = spark.read.format("delta").table("bronze.marca")
df_modelo    = spark.read.format("delta").table("bronze.modelo")
df_municipio = spark.read.format("delta").table("bronze.municipio")
df_regiao    = spark.read.format("delta").table("bronze.regiao")
df_sinistro  = spark.read.format("delta").table("bronze.sinistro")
df_telefone  = spark.read.format("delta").table("bronze.telefone")

# COMMAND ----------

# MAGIC %md
# MAGIC ## df = df_apolice.withColumn("nome_coluna", "valor")
# MAGIC
# MAGIC Adiciona uma nova coluna (metadado) de data e hora de processamento e nome do arquivo de origem.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_apolice   = df_apolice.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("apolice"))
df_carro     = df_carro.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("carro"))
df_cliente   = df_cliente.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("cliente"))
df_endereco  = df_endereco.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("endereco"))
df_estado    = df_estado.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("estado"))
df_marca     = df_marca.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("marca"))
df_modelo    = df_modelo.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("modelo"))
df_municipio = df_municipio.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("municipio"))
df_regiao    = df_regiao.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("regiao"))
df_sinistro  = df_sinistro.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_tabela", lit("sinistro"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## df_apolice.write.format('delta').saveAsTable("nome_tabela")
# MAGIC
# MAGIC Salva os dataframes em arquivos delta lake (formato de arquivo) no schema/database "bronze". As tabelas geradas são do tipo MANAGED (gerenciadas).

# COMMAND ----------

# df_apolice.write.format('delta').mode("overwrite").saveAsTable("bronze.apolice")
# df_carro.write.format('delta').mode("overwrite").saveAsTable("bronze.carro")
# df_cliente.write.format('delta').mode("overwrite").saveAsTable("bronze.cliente")
# df_endereco.write.format('delta').mode("overwrite").saveAsTable("bronze.endereco")
# df_estado.write.format('delta').mode("overwrite").saveAsTable("bronze.estado")
# df_marca.write.format('delta').mode("overwrite").saveAsTable("bronze.marca")
# df_modelo.write.format('delta').mode("overwrite").saveAsTable("bronze.modelo")
# df_municipio.write.format('delta').mode("overwrite").saveAsTable("bronze.municipio")
# df_regiao.write.format('delta').mode("overwrite").saveAsTable("bronze.regiao")
# df_sinistro.write.format('delta').mode("overwrite").saveAsTable("bronze.sinistro")
# df_telefone.write.format('delta').mode("overwrite").saveAsTable("bronze.telefone")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Maiusculas, tirando siglas, etc e gravando no formato delta no Silver
# MAGIC
# MAGIC Aplicando Data Quality

# COMMAND ----------

from pyspark.sql import functions as F

# ---------- Helpers ----------
def _apply_name_rules(colname: str) -> str:
    """Regras de renome: upper + prefixos 'CD_', 'VL_', etc."""
    n = colname.upper()
    n = n.replace("CD_", "CODIGO_")
    n = n.replace("VL_", "VALOR_")
    n = n.replace("DT_", "DATA_")
    n = n.replace("NM_", "NOME_")
    n = n.replace("DS_", "DESCRICAO_")
    n = n.replace("NR_", "NUMERO_")
    n = n.replace("_UF", "_UNIDADE_FEDERATIVA")
    return n

def _safe_drop(df, cols):
    """Dropa colunas somente se existirem."""
    existing = set(df.columns)
    to_drop = [c for c in cols if c in existing]
    return df.drop(*to_drop) if to_drop else df

# ---------- Core ----------
def renomear_colunas_managed(src_fqn: str, dest_fqn: str = None):
    """
    Lê uma managed table (Delta) do metastore, aplica regras de renome,
    ajusta colunas de auditoria e salva como **managed table** via saveAsTable.
    - src_fqn: 'schema.tabela' de origem (ex.: 'bronze.apolice')
    - dest_fqn: 'schema.tabela' de destino; se None, sobrescreve a própria origem
    """
    dest_fqn = dest_fqn or src_fqn

    # Lê como TABELA (managed)
    df = spark.read.format("delta").table(src_fqn)

    # Renomeia todas as colunas de uma vez (evita conflito de rename em loop)
    new_cols = [_apply_name_rules(c) for c in df.columns]
    df = df.toDF(*new_cols)

    # Remove colunas antigas, se existirem
    df = _safe_drop(df, ["DATA_HORA_BRONZE", "NOME_ARQUIVO"])

    # Adiciona colunas de auditoria pedidas
    df = (df
          .withColumn("NOME_ARQUIVO_BRONZE", F.lit(src_fqn))     # origem rastreável
          .withColumn("DATA_ARQUIVO_SILVER", F.current_timestamp())
         )

    # Salva como **Managed Table** (sem LOCATION) — sobrescrevendo destino
    (df.write
       .format("delta")
       .mode("overwrite")
       .saveAsTable(dest_fqn))

    return dest_fqn



# COMMAND ----------

renomear_colunas_managed("bronze.apolice",   "silver.apolice")
renomear_colunas_managed("bronze.carro",     "silver.carro")
renomear_colunas_managed("bronze.cliente",   "silver.cliente")
renomear_colunas_managed("bronze.endereco",  "silver.endereco")
renomear_colunas_managed("bronze.estado",    "silver.estado")
renomear_colunas_managed("bronze.marca",     "silver.marca")
renomear_colunas_managed("bronze.modelo",    "silver.modelo")
renomear_colunas_managed("bronze.municipio", "silver.municipio")
renomear_colunas_managed("bronze.regiao",    "silver.regiao")
renomear_colunas_managed("bronze.sinistro",  "silver.sinistro")
renomear_colunas_managed("bronze.telefone",  "silver.telefone")



# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN bronze
# MAGIC
# MAGIC Verifica os dados gravados no formato delta lake tipo MANAGED na camada bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE DETAIL nome_tabela;
# MAGIC
# MAGIC
# MAGIC Vendo os detalhes de um tabela delta lake.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL silver.apolice;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE EXTENDED nome_tabela;
# MAGIC ou 
# MAGIC ##(SQL) DESCRIBE TABLE EXTENDED nome_tabela;
# MAGIC
# MAGIC Mostra se a tabela é MANAGED Ou EXTERNAL.
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED silver.apolice;
# MAGIC --DESCRIBE TABLE EXTENDED apolice_bronze;