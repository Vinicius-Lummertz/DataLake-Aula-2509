# Projeto Lakehouse para Análise de Vendas de Restaurante

Este projeto demonstra a construção de um pipeline de dados ELT (Extract, Load, Transform) utilizando Databricks, seguindo a arquitetura Medalhão (Bronze, Silver, Gold) para processar e analisar dados de vendas de uma rede de restaurantes.

##  Arquitetura

O pipeline é orquestrado em três camadas principais:

1.  **Camada Landing/Bronze:** Os dados brutos (arquivos CSV) são ingeridos de um volume e carregados em tabelas Delta na camada Bronze, mantendo a estrutura original e adicionando metadados de auditoria.
2.  **Camada Silver:** Os dados da camada Bronze passam por um processo de limpeza, padronização de nomes de colunas, e enriquecimento, resultando em tabelas mais consistentes e prontas para análise.
3.  **Camada Gold:** A partir da camada Silver, é construído um modelo dimensional (Star Schema) otimizado para Business Intelligence e análises. Este modelo consiste em tabelas de dimensão (ex: `dim_franquia`, `dim_cardapio`) e uma tabela de fatos (`fato_vendas`).

## Estrutura do Repositório

-   `/notebooks`: Contém os notebooks Databricks para cada etapa do pipeline (Setup, Landing->Bronze, Bronze->Silver, Silver->Gold, Cleanup).
-   `/docs`: Documentação do projeto gerada com MkDocs.
-   `README.md`: Este arquivo.
-   `mkdocs.yml`: Arquivo de configuração para a documentação.

## Modelo de Dados (Camada Gold)

-   **`fato_vendas`**: Tabela central com as métricas de negócio (quantidade vendida, valor total).
-   **`dim_franquia`**: Dimensão com informações sobre as filiais do restaurante.
-   **`dim_profissional`**: Dimensão com os dados dos funcionários.
-   **`dim_cardapio`**: Dimensão contendo os pratos, preços e categorias.
-   **`dim_tempo`**: Dimensão de data para análises temporais.

## Como Executar o Pipeline

1.  **Configurar o Ambiente:** Execute o notebook `01_Setup_Ambiente.py` para criar os schemas e volumes necessários.
2.  **Upload dos Dados:** Faça o upload dos arquivos CSV (`franquias.csv`, `vendas.csv`, etc.) para o volume `workspace.landing.dados`.
3.  **Criar um Job no Databricks:**
    -   Crie um novo Job.
    -   Adicione três tarefas sequenciais, cada uma apontando para um notebook na seguinte ordem:
        1.  `02_Landing_para_Bronze.py`
        2.  `03_Bronze_para_Silver.py`
        3.  `04_Silver_para_Gold.py`
    -   Execute o Job para processar os dados através de todo o pipeline.
4.  **Análise:** Após a execução, os dados estarão disponíveis na camada Gold (`gold.fato_vendas`) para serem consumidos por ferramentas de BI ou notebooks de análise.