# Databricks notebook source
# MAGIC %md
# MAGIC ## display(dbutils.fs.ls('caminho')
# MAGIC
# MAGIC
# MAGIC Mostra todos os arquivos que estão dentro do Volume chamado "dados" que foi criado dentro do catálogo workspace, schema/database default.

# COMMAND ----------

display(dbutils.fs.ls('/'))

# COMMAND ----------

display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## df = spark.read.option("infeschema", "true").option("header", "true").csv("path + filename")
# MAGIC
# MAGIC Gera um dataframe para cada arquivo que está no Volume "dados".
# MAGIC

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados'

df_apolice   = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/apolice.csv")
df_carro     = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/carro.csv")
df_cliente   = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/cliente.csv")
df_endereco  = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/endereco.csv")
df_estado    = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/estado.csv")
df_marca     = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/marca.csv")
df_modelo    = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/modelo.csv")
df_municipio = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/municipio.csv")
df_regiao    = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/regiao.csv")
df_sinistro  = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/sinistro.csv")
df_telefone  = spark.read.option("infeschema", "true").option("header", "true").csv(f"{caminho_landing}/telefone.csv")


# COMMAND ----------

# MAGIC %md
# MAGIC ## df = df_apolice.withColumn("nome_coluna", "valor")
# MAGIC
# MAGIC Adiciona uma nova coluna (metadado) de data e hora de processamento e nome do arquivo de origem.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_apolice   = df_apolice.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("apolice.csv"))
df_carro     = df_carro.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("carro.csv"))
df_cliente   = df_cliente.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("cliente.csv"))
df_endereco  = df_endereco.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("endereco.csv"))
df_estado    = df_estado.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("estado.csv"))
df_marca     = df_marca.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("marca.csv"))
df_modelo    = df_modelo.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("modelo.csv"))
df_municipio = df_municipio.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("municipio.csv"))
df_regiao    = df_regiao.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("regiao.csv"))
df_sinistro  = df_sinistro.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("sinistro.csv"))
df_telefone  = df_telefone.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("telefone.csv"))


# COMMAND ----------

# MAGIC %md
# MAGIC ## df_apolice.write.format('delta').saveAsTable("nome_tabela")
# MAGIC
# MAGIC Salva os dataframes em arquivos delta lake (formato de arquivo) no schema/database "bronze". As tabelas geradas são do tipo MANAGED (gerenciadas).

# COMMAND ----------

df_apolice.write.format('delta').mode("overwrite").saveAsTable("bronze.apolice")
df_carro.write.format('delta').mode("overwrite").saveAsTable("bronze.carro")
df_cliente.write.format('delta').mode("overwrite").saveAsTable("bronze.cliente")
df_endereco.write.format('delta').mode("overwrite").saveAsTable("bronze.endereco")
df_estado.write.format('delta').mode("overwrite").saveAsTable("bronze.estado")
df_marca.write.format('delta').mode("overwrite").saveAsTable("bronze.marca")
df_modelo.write.format('delta').mode("overwrite").saveAsTable("bronze.modelo")
df_municipio.write.format('delta').mode("overwrite").saveAsTable("bronze.municipio")
df_regiao.write.format('delta').mode("overwrite").saveAsTable("bronze.regiao")
df_sinistro.write.format('delta').mode("overwrite").saveAsTable("bronze.sinistro")
df_telefone.write.format('delta').mode("overwrite").saveAsTable("bronze.telefone")

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN bronze
# MAGIC
# MAGIC Verifica os dados gravados no formato delta lake tipo MANAGED na camada bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bronze

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE DETAIL nome_tabela;
# MAGIC
# MAGIC
# MAGIC Vendo os detalhes de um tabela delta lake.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL bronze.apolice;
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
# MAGIC DESCRIBE EXTENDED bronze.apolice;
# MAGIC --DESCRIBE TABLE EXTENDED apolice_bronze;