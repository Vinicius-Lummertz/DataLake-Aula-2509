# Projeto Lakehouse: Análise de Vendas de Restaurante

Este projeto demonstra um pipeline de dados ELT (Extract, Load, Transform) completo construído no Databricks. O objetivo é processar dados de vendas de uma rede de restaurantes, desde a ingestão de dados brutos até a criação de um modelo dimensional (Star Schema) pronto para análise e Business Intelligence.

O pipeline utiliza a **Arquitetura Medalhão** (Bronze, Silver, Gold) e é totalmente orquestrado por notebooks Databricks, garantindo reprodutibilidade e escalabilidade.

---

## 🚀 Arquitetura Medalhão

O pipeline é dividido em três camadas lógicas de dados, cada uma com um propósito específico:

1.  **Camada Landing/Bronze**:
    * **Propósito**: Ingestão de dados brutos (Extract & Load).
    * **Processo**: Os dados de origem (simulados como CSVs) são carregados de um Volume (`workspace.landing.dados`) para tabelas Delta na camada Bronze (ex: `bronze.vendas`).
    * **Transformações**: Nenhuma transformação de negócio é aplicada. Apenas metadados de auditoria (como `data_hora_bronze` e `fonte_dados`) são adicionados.

2.  **Camada Silver**:
    * **Propósito**: Dados limpos, padronizados e enriquecidos (Transform).
    * **Processo**: As tabelas da Bronze são lidas e passam por um processo de limpeza.
    * **Transformações**: Renomeação de colunas (ex: `id_franquia` -> `SK_FRANQUIA`), padronização de tipos de dados, e validações de qualidade.

3.  **Camada Gold**:
    * **Propósito**: Modelo de dados de negócios, otimizado para análise (BI).
    * **Processo**: Os dados da Silver são agregados e modelados.
    * **Transformações**: Criação de um **Star Schema** com tabelas Fato (ex: `fato_vendas`) e Dimensão (ex: `dim_franquia`, `dim_cardapio`, `dim_tempo`).

---

## ⚙️ Orquestração e Execução

O pipeline é executado através de uma sequência de notebooks, que devem ser rodados na ordem correta.

### Ordem de Execução

1.  **`Notebooks/Setup.py`**:
    * **O que faz**: Prepara todo o ambiente. Primeiro, executa uma limpeza (`DROP SCHEMA ... CASCADE`) para garantir que o pipeline possa ser re-executado do zero.
    * **Criação**: `workspace.landing`, `workspace.bronze`, `workspace.silver`, `workspace.gold` e o Volume `workspace.landing.dados`.

2.  **`Notebooks/Landing-Bronze.py`**:
    * **O que faz**: Simula a ingestão de dados.
    * **Processo**:
        1.  Usa `dbutils.fs.put()` para criar os arquivos CSV (`vendas.csv`, `franquias.csv`, etc.) no Volume `workspace.landing.dados`.
        2.  Lê esses CSVs com `spark.read.csv()`.
        3.  Adiciona metadados de auditoria (`data_hora_bronze`).
        4.  Salva as tabelas em formato Delta no schema `bronze`.

3.  **`Notebooks/Bronze-Silver.py`**:
    * **O que faz**: Limpa e padroniza os dados.
    * **Processo**:
        1.  Lê as tabelas do schema `bronze`.
        2.  Aplica regras de renomeação (ex: `id_franquia` para `SK_FRANQUIA`).
        3.  Salva as tabelas limpas em formato Delta no schema `silver`.

4.  **`Notebooks/Silver-Gold.py`**:
    * **O que faz**: Constrói o modelo dimensional (Star Schema).
    * **Processo**:
        1.  Lê as tabelas do schema `silver`.
        2.  Cria as tabelas de Dimensão (`dim_franquia`, `dim_profissional`, `dim_cardapio`, `dim_tempo`).
        3.  Usa `MERGE INTO` para carregar os dados nas dimensões (SCD Tipo 1).
        4.  Cria a tabela `fato_vendas` e a popula fazendo join com as dimensões para obter as chaves substitutas (SKs).

### Notebooks Auxiliares

* **`Notebooks/ShowTables.py`**: Um notebook simples de consulta para visualizar os resultados finais nas tabelas `gold.*`.
* **`Notebooks/Cleanup.py`**: Um notebook autônomo para limpar completamente todos os schemas (`landing`, `bronze`, `silver`, `gold`) do ambiente.

---

## 📊 Modelo de Dados (Camada Gold)

O produto final do pipeline é um Star Schema otimizado para consultas analíticas:

* **Tabela Fato**: `fato_vendas`
* **Tabelas de Dimensão**:
    * `dim_franquia`
    * `dim_profissional`
    * `dim_cardapio`
    * `dim_tempo`

---

## 📖 Documentação (MkDocs)

Este projeto inclui uma documentação detalhada gerada com MkDocs. Para visualizar:

1.  Instale o MkDocs e o tema Material:
    ```bash
    pip install mkdocs mkdocs-material
    ```
2.  Navegue até o diretório `DataBricks/Restaurante` (onde o `mkdocs.yml` está).
3.  Execute o servidor local:
    ```bash
    mkdocs serve
    ```
4.  Abra `http://127.0.0.1:8000` no seu navegador.