# Demonstração com Apache Iceberg

Apache Iceberg é um formato de tabela aberta para enormes conjuntos de dados analíticos. O Iceberg gerencia grandes coleções de arquivos como tabelas e suporta mecanismos de processamento de dados modernos.

## DDL (Data Definition Language)

Para o Iceberg, criamos a tabela dentro do nosso catálogo `local_iceberg`, no banco de dados `restaurante`.

```sql
CREATE TABLE local_iceberg.restaurante.pratos_iceberg (
  id INT,
  nome_prato STRING,
  categoria STRING,
  ingredientes ARRAY<STRING>,
  preco DECIMAL(10, 2),
  disponivel BOOLEAN
) USING iceberg