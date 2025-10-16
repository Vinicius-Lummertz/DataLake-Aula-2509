# Databricks notebook source
# MAGIC %md
# MAGIC ### Setup do Ambiente Lakehouse - Projeto Restaurante
# MAGIC 
# MAGIC Criando os schemas e o volume para o pipeline de dados.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Schema para receber os dados brutos (arquivos CSV)
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.landing
# MAGIC COMMENT 'Schema para dados brutos (landing zone)';
# MAGIC 
# MAGIC -- Volume para armazenar os arquivos brutos
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.landing.dados
# MAGIC COMMENT 'Volume para arquivos brutos do projeto restaurante';
# MAGIC 
# MAGIC -- Schema para as tabelas Delta da camada Bronze
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.bronze
# MAGIC COMMENT 'Schema para dados na camada Bronze (Delta)';
# MAGIC 
# MAGIC -- Schema para as tabelas Delta da camada Silver
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.silver
# MAGIC COMMENT 'Schema para dados na camada Silver (Delta)';
# MAGIC 
# MAGIC -- Schema para o modelo dimensional na camada Gold
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.gold
# MAGIC COMMENT 'Schema para dados na camada Gold (Delta) - Modelagem Dimensional';