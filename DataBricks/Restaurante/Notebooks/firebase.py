# Databricks notebook source
# MAGIC %pip install firebase-admin

# COMMAND ----------

# É necessário reiniciar o kernel para que o Databricks reconheça a nova biblioteca
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Garante que o catálogo 'workspace' (que parece ser o padrão do seu ambiente) esteja em uso.
# MAGIC USE CATALOG workspace;
# MAGIC
# MAGIC -- Cria o schema 'bronze' se ele ainda não existir.
# MAGIC -- Isso previne o erro 'SCHEMA_NOT_FOUND' na próxima etapa.
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze
# MAGIC COMMENT 'Schema para dados brutos (bronze) ingeridos do Firebase';

# COMMAND ----------

import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import io

# --- CONFIGURAÇÃO ---
CAMINHO_CHAVE_JSON = "/Workspace/Users/vinicius.902120@alunosatc.edu.br/firebase.json" # <--- ATUALIZE AQUI

# Inicialização do Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(CAMINHO_CHAVE_JSON)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Conectado ao Firebase com sucesso.")
except Exception as e:
    print(f"Erro na conexão: {e}")
    dbutils.notebook.exit("Pare e verifique a chave JSON.")

# --- DADOS BRUTOS (Strings do seu exemplo) ---
csv_franquias = """id_franquia,nome_franquia,cidade,estado
1,Restaurante Matriz SP,São Paulo,SP
2,Filial Campinas,Campinas,SP
3,Filial Rio de Janeiro,Rio de Janeiro,RJ
4,Filial Curitiba,Curitiba,PR
5,Filial Belo Horizonte,Belo Horizonte,MG"""

csv_profissionais = """id_profissional,id_franquia,nome_profissional,cargo
1,4,Funcionario_1,Caixa
2,2,Funcionario_2,Gerente
3,3,Funcionario_3,Cozinheiro
4,4,Funcionario_4,Auxiliar de Cozinha
5,4,Funcionario_5,Gerente
6,5,Funcionario_6,Garçom
7,2,Funcionario_7,Cozinheiro
8,1,Funcionario_8,Caixa
9,3,Funcionario_9,Gerente
10,4,Funcionario_10,Caixa
11,4,Funcionario_11,Cozinheiro
12,2,Funcionario_12,Caixa
13,2,Funcionario_13,Gerente
14,4,Funcionario_14,Gerente
15,3,Funcionario_15,Caixa
16,2,Funcionario_16,Cozinheiro
17,2,Funcionario_17,Caixa
18,1,Funcionario_18,Auxiliar de Cozinha
19,1,Funcionario_19,Gerente
20,3,Funcionario_20,Caixa"""

csv_cardapio = """id_prato,nome_prato,preco,categoria
201,Prato Feito (PF),25.0,Principal
202,Hambúrguer Clássico,30.5,Lanche
203,Pizza de Muçarela,45.0,Pizza
204,Salada Caesar,22.0,Salada
205,Porção de Batata Frita,15.0,Acompanhamento
206,Frango Grelhado,28.0,Principal
207,Refrigerante Lata,6.0,Bebida
208,Suco Natural,8.5,Bebida"""

csv_ingredientes = """id_ingrediente,nome_ingrediente
101,Tomate
102,Queijo Muçarela
103,Farinha de Trigo
104,Carne Bovina
105,Alface
106,Pão de Hambúrguer
107,Batata
108,Frango
109,Arroz
110,Feijão
111,Cebola
112,Óleo Vegetal"""

csv_vendas = """id_venda,id_franquia,id_profissional,id_prato,data_venda,quantidade,valor_total
1,1,13,203,2024-09-30,1,45.0
2,3,2,207,2024-06-20,3,18.0
3,4,1,205,2024-08-12,3,45.0
4,4,17,203,2024-03-30,2,90.0
5,2,8,202,2024-10-18,2,61.0
6,4,16,206,2024-04-22,3,84.0
7,4,12,204,2024-05-30,3,66.0
8,5,2,204,2024-07-09,3,66.0
9,2,4,202,2024-06-25,3,91.5
10,2,17,207,2024-06-04,3,18.0
11,3,4,206,2024-07-09,3,84.0
12,3,10,202,2024-03-20,2,61.0
13,5,16,206,2024-09-08,1,28.0
14,4,18,208,2024-07-05,1,8.5
15,3,1,203,2024-06-03,3,135.0
16,1,3,204,2024-10-02,2,44.0
17,4,17,202,2024-08-11,2,61.0
18,4,1,201,2024-10-25,2,50.0
19,2,7,208,2024-06-10,2,17.0
20,1,2,204,2024-04-30,3,66.0
21,3,20,201,2024-01-23,2,50.0
22,1,19,203,2024-08-02,2,90.0
23,4,5,202,2024-07-13,1,30.5
24,1,11,203,2024-07-04,1,45.0
25,3,11,203,2024-04-07,2,90.0
26,3,6,205,2024-02-25,2,30.0
27,3,9,203,2024-07-05,3,135.0
28,2,4,205,2024-05-09,2,30.0
29,2,5,205,2024-09-14,1,15.0
30,1,19,203,2024-06-13,2,90.0
31,1,20,208,2024-10-01,1,8.5
32,4,13,204,2024-05-20,1,22.0
33,3,1,207,2024-04-08,1,6.0
34,5,4,206,2024-03-11,1,28.0
35,4,16,208,2024-05-06,1,8.5
36,5,17,203,2024-01-30,3,135.0
37,4,5,202,2024-09-18,1,30.5
38,2,5,202,2024-07-17,3,91.5
39,1,5,206,2024-07-10,2,56.0
40,1,18,203,2024-07-29,3,135.0
41,1,9,207,2024-09-20,3,18.0
42,1,5,206,2024-08-21,2,56.0
43,2,1,202,2024-06-26,1,30.5
44,4,15,208,2024-08-15,1,8.5
45,1,14,205,2024-07-08,1,15.0
46,4,20,205,2024-08-28,3,45.0
47,2,11,208,2024-01-01,2,17.0
48,3,11,208,2024-06-09,3,25.5
49,5,12,208,2024-05-21,1,8.5
50,4,10,204,2024-08-10,1,22.0"""

# --- FUNÇÃO DE UPLOAD ---
def upload_string_csv_to_firebase(csv_string, nome_colecao, id_coluna):
    print(f"Processando coleção: {nome_colecao}...")
    # 1. Converter String CSV para Pandas (memória)
    pdf = pd.read_csv(io.StringIO(csv_string))
    
    # 2. Preparar Batch do Firestore
    batch = db.batch()
    contador = 0
    
    # 3. Iterar e Adicionar ao Batch
    for index, row in pdf.iterrows():
        dados = row.to_dict()
        doc_id = str(dados[id_coluna]) # ID deve ser string
        
        # Converter tipos numéricos do NumPy para tipos nativos do Python
        # Isso evita erros de serialização do Firestore com int64/float64
        dados_limpos = {}
        for k, v in dados.items():
            if pd.isna(v):
                dados_limpos[k] = None
            elif hasattr(v, 'item'): # Checa se é um tipo NumPy
                dados_limpos[k] = v.item()
            else:
                dados_limpos[k] = v
        
        doc_ref = db.collection(nome_colecao).document(doc_id)
        batch.set(doc_ref, dados_limpos)
        contador += 1
        
        # Limite de 500 operações por batch
        if contador % 400 == 0:
            batch.commit()
            batch = db.batch()
            
    # Commit final
    if contador % 400 != 0:
        batch.commit()
    print(f"  -> Sucesso! {contador} registros enviados para '{nome_colecao}'.")

# --- EXECUÇÃO DA CARGA ---
print(">>> INICIANDO UPLOAD PARA O FIREBASE <<<")
upload_string_csv_to_firebase(csv_franquias, "franquias", "id_franquia")
upload_string_csv_to_firebase(csv_profissionais, "profissionais", "id_profissional")
upload_string_csv_to_firebase(csv_cardapio, "cardapio", "id_prato")
upload_string_csv_to_firebase(csv_ingredientes, "ingredientes", "id_ingrediente")
upload_string_csv_to_firebase(csv_vendas, "vendas", "id_venda")
print(">>> UPLOAD CONCLUÍDO <<<")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.types import StructType # Necessário para o caso de coleção vazia

def carregar_firebase_para_delta(nome_colecao, nome_tabela):
    print(f"Baixando coleção '{nome_colecao}' do Firebase...")
    
    # 1. Ler do Firebase
    # A variável 'db' foi definida globalmente no Bloco 4.
    # A verificação 'if "db" not in locals()' foi removida por ser incorreta.
    
    # Esta linha agora usará a variável 'db' global criada no Bloco 4.
    docs = db.collection(nome_colecao).stream()
    lista_dados = [doc.to_dict() for doc in docs]
    
    if not lista_dados:
        print(f"  -> Aviso: Coleção '{nome_colecao}' está vazia. Nenhuma tabela será criada.")
        return

    # 2. Converter para Spark DataFrame via Pandas
    pdf_temp = pd.DataFrame(lista_dados)
    print(lista_dados)
    # Corrigir tipos de dados que o Spark pode inferir errado (ex: int como double)
    for col in pdf_temp.columns:
        # Se uma coluna parece ser ID ou quantidade, tenta converter para Inteiro (lidando com NAs)
        if 'id' in col or 'quantidade' in col:
            pdf_temp[col] = pd.to_numeric(pdf_temp[col], errors='coerce').astype('Int64') # Int64 aceita <NA>
        # Se for preço ou valor, converte para float
        elif 'preco' in col or 'valor' in col:
             pdf_temp[col] = pd.to_numeric(pdf_temp[col], errors='coerce').astype('float64')

    
    sdf = spark.createDataFrame(pdf_temp)
    
    # 3. Adicionar colunas de auditoria
    sdf = sdf.withColumn("data_carga_bronze", current_timestamp()) \
             .withColumn("origem_dados", lit("firebase_firestore"))

    # 4. Salvar como Tabela Delta (Bronze)
    # O Bloco 3 já garantiu que `workspace.bronze` existe
    caminho_tabela = f"workspace.bronze.{nome_tabela}"
    print(f"  -> Salvando tabela Delta: {caminho_tabela}")
    
    (sdf.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(caminho_tabela)
    )
    print("  -> Tabela criada com sucesso!")

# --- EXECUÇÃO DO DOWNLOAD ---
print(">>> INICIANDO CRIAÇÃO DAS TABELAS BRONZE <<<")
carregar_firebase_para_delta("franquias", "franquias")
carregar_firebase_para_delta("profissionais", "profissionais")
carregar_firebase_para_delta("cardapio", "cardapio")
carregar_firebase_para_delta("ingredientes", "ingredientes")
carregar_firebase_para_delta("vendas", "vendas")
print(">>> PROCESSO FINALIZADO <<<")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.bronze.vendas LIMIT 10;