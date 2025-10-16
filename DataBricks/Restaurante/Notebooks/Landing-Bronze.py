# Databricks notebook source
# MAGIC %md
# MAGIC ## Pipeline Restaurante: Landing para Bronze
# MAGIC 
# MAGIC Lendo os arquivos CSV do volume e salvando como tabelas Delta na camada Bronze.

# COMMAND ----------

# Verifica se os arquivos foram carregados no volume
display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Leitura dos arquivos CSV

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados'

df_franquias = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/franquias.csv")
df_profissionais = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/profissionais.csv")
df_ingredientes = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/ingredientes.csv")
df_cardapio = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/cardapio.csv")
df_vendas = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/vendas.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Adicionando Metadados de Auditoria

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_franquias = df_franquias.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("franquias.csv"))
df_profissionais = df_profissionais.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("profissionais.csv"))
df_ingredientes = df_ingredientes.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("ingredientes.csv"))
df_cardapio = df_cardapio.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("cardapio.csv"))
df_vendas = df_vendas.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("vendas.csv"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Salvando como Tabelas Delta na Camada Bronze

# COMMAND ----------

df_franquias.write.format('delta').mode("overwrite").saveAsTable("bronze.franquias")
df_profissionais.write.format('delta').mode("overwrite").saveAsTable("bronze.profissionais")
df_ingredientes.write.format('delta').mode("overwrite").saveAsTable("bronze.ingredientes")
df_cardapio.write.format('delta').mode("overwrite").saveAsTable("bronze.cardapio")
df_vendas.write.format('delta').mode("overwrite").saveAsTable("bronze.vendas")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bronze;