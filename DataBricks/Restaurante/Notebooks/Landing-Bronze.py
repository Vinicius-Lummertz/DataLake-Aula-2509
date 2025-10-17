# Databricks notebook source
# MAGIC %md
# MAGIC # 1. Ingestão de Dados do PostgreSQL (Render) para a Camada Bronze
# MAGIC 
# MAGIC Este notebook é responsável por:
# MAGIC 1.  Conectar-se a um banco de dados PostgreSQL externo na nuvem (Render).
# MAGIC 2.  **Popular** o banco com dados de exemplo do restaurante (usando Pandas e SQLAlchemy).
# MAGIC 3.  **Ler** os dados do PostgreSQL para DataFrames Spark usando JDBC.
# MAGIC 4.  Salvar os DataFrames como tabelas Delta na camada **Bronze**.
# MAGIC 
# MAGIC **AVISO:** As credenciais estão inseridas diretamente no código para fins de demonstração. Em um ambiente de produção, use o Databricks Secrets.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 1: Instalação das Bibliotecas Necessárias
# MAGIC 
# MAGIC `psycopg2-binary` é o driver que permite ao Python se comunicar com o PostgreSQL.
# MAGIC `SQLAlchemy` é uma biblioteca que facilita a interação com bancos de dados SQL.

# COMMAND ----------

%pip install psycopg2-binary SQLAlchemy pandas

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 2: Configuração das Credenciais (Inseridas Diretamente)
# MAGIC 
# MAGIC Carregando as credenciais do banco de dados em variáveis.

# COMMAND ----------

# Configurações do banco de dados
db_host = "dpg-d3namjbe5dus738skudg-a.oregon-postgres.render.com"
db_user = "football_predictor_user"
db_pass = "JbHXfhQe9iQsxoK42TpaoysYiCt5GthQ"
db_port = "5432"
db_name = "football_predictor"

# Montando a URL de conexão JDBC para o Spark
jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

print("Credenciais configuradas no código.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 3: População do Banco de Dados Externo
# MAGIC 
# MAGIC Esta etapa usa **Pandas** e **SQLAlchemy** para criar as tabelas e inserir os dados no seu banco no Render.
# MAGIC A opção `if_exists='replace'` fará com que as tabelas sejam recriadas a cada execução.

# COMMAND ----------

import pandas as pd
from sqlalchemy import create_engine

# Criando a engine de conexão com SQLAlchemy
db_conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_conn_string)

print("Conexão com SQLAlchemy estabelecida.")

# --- Dados do Restaurante (mesmos dos CSVs) ---

# 1. Franquias
franquias_data = {
    'id_franquia': [1, 2, 3, 4, 5],
    'nome_franquia': ['Restaurante Matriz SP', 'Filial Campinas', 'Filial Rio de Janeiro', 'Filial Curitiba', 'Filial Belo Horizonte'],
    'cidade': ['São Paulo', 'Campinas', 'Rio de Janeiro', 'Curitiba', 'Belo Horizonte'],
    'estado': ['SP', 'SP', 'RJ', 'PR', 'MG']
}
df_franquias = pd.DataFrame(franquias_data)
df_franquias.to_sql('franquias', engine, if_exists='replace', index=False)
print("Tabela 'franquias' populada com sucesso.")

# 2. Cardápio
cardapio_data = {
    'id_prato': [201, 202, 203, 204, 205, 206, 207, 208],
    'nome_prato': ['Prato Feito (PF)', 'Hambúrguer Clássico', 'Pizza de Muçarela', 'Salada Caesar', 'Porção de Batata Frita', 'Frango Grelhado', 'Refrigerante Lata', 'Suco Natural'],
    'preco': [25.00, 30.50, 45.00, 22.00, 15.00, 28.00, 6.00, 8.50],
    'categoria': ['Principal', 'Lanche', 'Pizza', 'Salada', 'Acompanhamento', 'Principal', 'Bebida', 'Bebida']
}
df_cardapio = pd.DataFrame(cardapio_data)
df_cardapio.to_sql('cardapio', engine, if_exists='replace', index=False)
print("Tabela 'cardapio' populada com sucesso.")

# 3. Profissionais
profissionais_data = {'id_profissional': range(1, 21), 'id_franquia': [ (i % 5) + 1 for i in range(20)], 'nome_profissional': [f'Funcionario_{i}' for i in range(1, 21)], 'cargo': ['Cozinheiro', 'Garçom', 'Gerente', 'Caixa', 'Auxiliar de Cozinha'] * 4}
df_profissionais = pd.DataFrame(profissionais_data)
df_profissionais.to_sql('profissionais', engine, if_exists='replace', index=False)
print("Tabela 'profissionais' populada com sucesso.")

# 4. Vendas
vendas_data = {
    'id_venda': range(1, 51), 'id_franquia': [(i % 5) + 1 for i in range(50)], 'id_profissional': [(i % 20) + 1 for i in range(50)],
    'id_prato': [201, 202, 203, 204, 205, 206, 207, 208] * (50//8) + [201, 202],
    'data_venda': pd.to_datetime(pd.date_range(start='2025-01-01', periods=50)), 'quantidade': [ (i % 3) + 1 for i in range(50)],
    'valor_total': [ 25.0, 30.5, 45.0, 22.0, 15.0, 28.0, 6.0, 8.5] * (50//8) + [25.0, 30.5]
}
df_vendas = pd.DataFrame(vendas_data)
df_vendas.to_sql('vendas', engine, if_exists='replace', index=False)
print("Tabela 'vendas' populada com sucesso.")

# 5. Ingredientes
ingredientes_data = {'id_ingrediente': range(101, 113), 'nome_ingrediente': ['Tomate', 'Queijo Muçarela', 'Farinha de Trigo', 'Carne Bovina', 'Alface', 'Pão de Hambúrguer', 'Batata', 'Frango', 'Arroz', 'Feijão', 'Cebola', 'Óleo Vegetal']}
df_ingredientes = pd.DataFrame(ingredientes_data)
df_ingredientes.to_sql('ingredientes', engine, if_exists='replace', index=False)
print("Tabela 'ingredientes' populada com sucesso.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 4: Leitura das Tabelas do PostgreSQL com Spark
# MAGIC 
# MAGIC Agora, usamos o **Spark** para ler os dados que acabamos de inserir no banco de dados.

# COMMAND ----------

# Configurações de conexão para o Spark
connection_properties = {
  "user": db_user,
  "password": db_pass,
  "driver": "org.postgresql.Driver"
}

# Lendo cada tabela para um DataFrame Spark
sdf_franquias     = spark.read.jdbc(url=jdbc_url, table="franquias", properties=connection_properties)
sdf_profissionais = spark.read.jdbc(url=jdbc_url, table="profissionais", properties=connection_properties)
sdf_cardapio      = spark.read.jdbc(url=jdbc_url, table="cardapio", properties=connection_properties)
sdf_ingredientes  = spark.read.jdbc(url=jdbc_url, table="ingredientes", properties=connection_properties)
sdf_vendas        = spark.read.jdbc(url=jdbc_url, table="vendas", properties=connection_properties)

print("DataFrames Spark criados a partir do PostgreSQL.")
display(sdf_vendas.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 5: Carga dos Dados na Camada Bronze
# MAGIC 
# MAGIC Com os DataFrames em memória, adicionamos metadados de auditoria e salvamos como tabelas Delta na camada Bronze.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# Adicionando metadados de auditoria
source_name = "PostgreSQL_Render_DB"

sdf_franquias     = sdf_franquias.withColumn("data_hora_bronze", current_timestamp()).withColumn("fonte_dados", lit(source_name))
sdf_profissionais = sdf_profissionais.withColumn("data_hora_bronze", current_timestamp()).withColumn("fonte_dados", lit(source_name))
sdf_cardapio      = sdf_cardapio.withColumn("data_hora_bronze", current_timestamp()).withColumn("fonte_dados", lit(source_name))
sdf_ingredientes  = sdf_ingredientes.withColumn("data_hora_bronze", current_timestamp()).withColumn("fonte_dados", lit(source_name))
sdf_vendas        = sdf_vendas.withColumn("data_hora_bronze", current_timestamp()).withColumn("fonte_dados", lit(source_name))

# Salvando as tabelas na camada Bronze
sdf_franquias.write.format('delta').mode("overwrite").saveAsTable("bronze.franquias")
sdf_profissionais.write.format('delta').mode("overwrite").saveAsTable("bronze.profissionais")
sdf_cardapio.write.format('delta').mode("overwrite").saveAsTable("bronze.cardapio")
sdf_ingredientes.write.format('delta').mode("overwrite").saveAsTable("bronze.ingredientes")
sdf_vendas.write.format('delta').mode("overwrite").saveAsTable("bronze.vendas")

print("Tabelas salvas com sucesso na camada Bronze.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Passo 6: Verificação
# MAGIC 
# MAGIC Vamos confirmar que as tabelas foram criadas corretamente na camada Bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SHOW TABLES IN bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT * FROM bronze.vendas LIMIT 10;