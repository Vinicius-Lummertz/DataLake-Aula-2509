# Databricks notebook source
# MAGIC %md
# MAGIC # Visualização das Tabelas Finais (Camada Gold) - Projeto Restaurante
# MAGIC 
# MAGIC Este notebook serve para visualizar os dados consolidados e modelados na camada Gold do nosso Lakehouse. As tabelas abaixo representam o modelo dimensional pronto para análises de BI.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Tabela de Dimensão: `dim_franquia`
# MAGIC 
# MAGIC Esta tabela contém os detalhes de cada filial do restaurante.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.dim_franquia;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Tabela de Dimensão: `dim_profissional`
# MAGIC 
# MAGIC Esta tabela contém a lista de profissionais (funcionários) da rede.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.dim_profissional;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Tabela de Dimensão: `dim_cardapio`
# MAGIC 
# MAGIC Contém todos os itens do cardápio, com seus respectivos preços e categorias.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.dim_cardapio;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Tabela de Dimensão: `dim_tempo`
# MAGIC 
# MAGIC Tabela de dimensão de data para permitir análises baseadas no tempo (diárias, mensais, anuais, etc.).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.dim_tempo
# MAGIC ORDER BY DATA DESC -- Mostrando as datas mais recentes primeiro
# MAGIC LIMIT 200;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Tabela Fato: `fato_vendas`
# MAGIC 
# MAGIC Tabela central do nosso modelo, contendo as métricas de negócio (quantidade e valor total) conectadas às dimensões através das chaves estrangeiras (FK).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.fato_vendas
# MAGIC LIMIT 200;