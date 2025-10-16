# Databricks notebook source
# MAGIC %md
# MAGIC ### Limpeza Completa do Ambiente do Pipeline
# MAGIC 
# MAGIC Remove todos os schemas (e suas tabelas/volumes) criados pelo pipeline.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP SCHEMA IF EXISTS workspace.bronze CASCADE;
# MAGIC DROP SCHEMA IF EXISTS workspace.silver CASCADE;
# MAGIC DROP SCHEMA IF EXISTS workspace.gold CASCADE;
# MAGIC DROP SCHEMA IF EXISTS workspace.landing CASCADE;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Confirma se todos os schemas foram removidos
# MAGIC SHOW SCHEMAS IN workspace;