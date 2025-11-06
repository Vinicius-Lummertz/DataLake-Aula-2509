# Detalhes dos Notebooks

O pipeline é composto por uma série de notebooks, projetados para serem executados sequencialmente.

### Ordem de Execução

1.  **[Setup](00_setup.md)**: Limpa e cria os schemas e volumes.
2.  **[Landing-Bronze](01_landing_bronze.md)**: Ingesta dados brutos para a camada Bronze.
3.  **[Bronze-Silver](02_bronze_silver.md)**: Limpa e padroniza os dados na camada Silver.
4.  **[Silver-Gold](03_silver_gold.md)**: Modela os dados da Silver para a camada Gold (Star Schema).

### Notebooks Utilitários

* **[ShowTables e Cleanup](99_utilitarios.md)**: Notebooks para visualizar resultados e limpar o ambiente.