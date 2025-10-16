# Databricks notebook source


# COMMAND ----------

# MAGIC %md
# MAGIC ### (database/schema) catalogo.schema
# MAGIC ### (volume) catalogo.schema.volume
# MAGIC
# MAGIC Criando volumes e schemas/databases

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Apagar todas as tabelas da camada bronze
# MAGIC DROP SCHEMA IF EXISTS workspace.bronze CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas da camada silver
# MAGIC DROP SCHEMA IF EXISTS workspace.silver CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas da camada gold
# MAGIC DROP SCHEMA IF EXISTS workspace.gold CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas e volumes da camada landing
# MAGIC DROP SCHEMA IF EXISTS workspace.landing CASCADE;
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW SCHEMAS IN catalogo;
# MAGIC
# MAGIC Confirmar se tudo foi limpo

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;