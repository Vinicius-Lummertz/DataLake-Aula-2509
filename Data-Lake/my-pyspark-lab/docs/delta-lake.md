# Demonstração com Delta Lake

Delta Lake é um formato de armazenamento de código aberto que traz transações ACID para o Apache Spark e cargas de trabalho de big data.

## DDL (Data Definition Language)

O comando `CREATE TABLE` abaixo define a estrutura da nossa tabela de pratos no formato Delta.

```sql
CREATE TABLE pratos_delta (
  id INT,
  nome_prato STRING,
  categoria STRING,
  ingredientes ARRAY<STRING>,
  preco DECIMAL(10, 2),
  disponivel BOOLEAN
) USING delta