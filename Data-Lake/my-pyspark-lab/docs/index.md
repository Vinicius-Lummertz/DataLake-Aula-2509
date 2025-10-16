# Projeto de Pesquisa: Apache Spark com Delta Lake e Iceberg

Bem-vindo à documentação do projeto.

Este site documenta o ambiente de desenvolvimento e demonstra o uso dos formatos de tabela de Lakehouse, Delta Lake e Apache Iceberg, com Apache Spark.

## Cenário: Gerenciamento de um Restaurante

O cenário escolhido para as demonstrações é o gerenciamento do cardápio de um restaurante. A tabela `pratos` armazena informações sobre cada item do menu, como nome, categoria, ingredientes, preço e disponibilidade.

### Modelo da Tabela `pratos`

-   **id**: (INT) Identificador único do prato.
-   **nome_prato**: (STRING) Nome do prato.
-   **categoria**: (STRING) Categoria (ex: Massas, Carnes, Sobremesas).
-   **ingredientes**: (ARRAY<STRING>) Lista de ingredientes principais.
-   **preco**: (DECIMAL) Preço do prato.
-   **disponivel**: (BOOLEAN) Se o prato está disponível no momento.    