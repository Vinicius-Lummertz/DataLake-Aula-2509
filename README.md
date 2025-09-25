Este projeto configura um ambiente de desenvolvimento local e autocontido para trabalhar com **Apache Spark (PySpark)**, **Delta Lake** e **Apache Iceberg** dentro de um **Jupyter Lab**. A gestão de dependências e do ambiente virtual é feita com o **Poetry**, garantindo um setup limpo e 100% reprodutível.

O objetivo é fornecer uma "caixa de areia" para estudar, testar e desenvolver soluções de Data Lakehouse sem a necessidade de configurar um cluster complexo na nuvem.

---

## ✨ Tecnologias e Versões

A reprodutibilidade é garantida pelo uso de versões específicas das principais ferramentas:

| Tecnologia | Versão | Propósito |
| :--- | :--- | :--- |
| **Python** | `3.9+` | Linguagem base |
| **Poetry** | `1.8+` | Gerenciador de dependências |
| **Apache Spark** | `3.5.0` | Motor de processamento distribuído |
| **Jupyter Lab** | `4.x` | IDE interativa baseada na web |
| **Delta Lake** | `3.2.0` | Formato de tabela transacional |
| **Apache Iceberg** | `1.5.2` | Formato de tabela aberta para grandes datasets |
| **Java (JDK)** | `11` ou `17` | Requisito para rodar o Spark (JVM) |

---

## 📂 Estrutura de Diretórios

O projeto está organizado da seguinte forma:

```
my-pyspark-lab/
├── notebooks/
│   └── 01-testing-formats.ipynb   # Notebook de exemplo para testar os formatos
├── warehouse/
│   ├── delta/                     # Armazenamento local para tabelas Delta
│   └── iceberg/                   # Armazenamento local para tabelas Iceberg
├── .gitignore                     # Arquivo para ignorar arquivos do Git
├── pyproject.toml                 # Arquivo de configuração do Poetry
├── README.md                      # Este arquivo
└── start-jupyter.sh               # Script para iniciar o ambiente
```

---

## 🔧 Pré-requisitos

Antes de começar, garanta que os seguintes softwares estejam instalados em seu sistema:

1.  **Python 3.9 ou superior**
    -   Verifique com: `python3 --version`
    -   [Instalar Python](https://www.python.org/downloads/)

2.  **Poetry**
    -   Verifique com: `poetry --version`
    -   [Instalar Poetry](https://python-poetry.org/docs/#installation) (o método com `curl` é recomendado)

3.  **Java Development Kit (JDK) 11 ou 17**
    -   Verifique com: `java -version`
    -   O Apache Spark precisa de uma Java Virtual Machine (JVM) para ser executado.
    -   Recomendamos o [OpenJDK](https://openjdk.java.net/install/).

---

## ⚙️ Passo a Passo para Configuração

Siga os passos abaixo para clonar e configurar o ambiente em sua máquina local.

### 1. Clone o Repositório

Primeiro, clone este projeto para a sua máquina.

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd my-pyspark-lab
```

### 2. Instale as Dependências Python

Use o Poetry para criar o ambiente virtual e instalar todas as bibliotecas Python listadas no arquivo `pyproject.toml`.

```bash
poetry install
```
Este comando irá ler o arquivo `pyproject.toml`, resolver as dependências e instalá-las em um ambiente virtual isolado, específico para este projeto.

### 3. Torne o Script de Inicialização Executável

O script `start-jupyter.sh` precisa de permissão de execução. Este passo é necessário apenas uma vez. (Para ambientes Linux/macOS/WSL).

```bash
chmod +x start-jupyter.sh
```

### 4. Inicie o Ambiente Jupyter Lab

Execute o script para iniciar o ambiente. Ele irá configurar todas as variáveis de ambiente necessárias para o Spark e depois abrir o Jupyter Lab.

```bash
./start-jupyter.sh
```
> **💡 Nota:** Na primeira vez que você executar este comando, o Spark levará alguns minutos para baixar os conectores (JARs) do Delta Lake e do Iceberg da internet. Isso é normal e só acontece uma vez.

Após a inicialização, o Jupyter Lab será aberto automaticamente no seu navegador.

### 5. Execute o Notebook de Teste

1.  No Jupyter Lab, navegue até a pasta `notebooks/`.
2.  Abra o arquivo `01-testing-formats.ipynb`.
3.  Execute todas as células do notebook para confirmar que a sessão Spark é criada corretamente e que você pode ler e escrever tabelas nos formatos Delta e Iceberg.

Se todas as células forem executadas sem erro, seu ambiente está configurado e pronto para uso! ✅

---

## 🔍 Como Funciona?

A "mágica" deste ambiente está no script `start-jupyter.sh`. Ele configura a variável de ambiente `PYSPARK_SUBMIT_ARGS`, que passa uma série de parâmetros diretamente para o Spark no momento em que ele é iniciado pelo Jupyter.

Os parâmetros mais importantes são:

-   `--packages`: Informa ao Spark quais JARs de projetos externos (neste caso, os conectores do Delta e do Iceberg) ele deve baixar do repositório Maven.
-   `--conf spark.sql.extensions`: Registra as extensões SQL para que o Spark entenda os novos comandos e sintaxes introduzidos por cada formato (ex: `UPDATE`, `MERGE` do Delta e `ALTER TABLE` do Iceberg).
-   `--conf spark.sql.catalog...`: Configura os catálogos do Spark. Aqui, definimos o catálogo padrão (`spark_catalog`) para ser o do Delta Lake e criamos um catálogo separado chamado `local_iceberg` para gerenciar as tabelas Iceberg, apontando para o nosso diretório `warehouse/iceberg`.

Ao executar o script antes do Jupyter, garantimos que qualquer notebook iniciado nesta sessão já terá uma sessão Spark pré-configurada e pronta para usar os formatos de Lakehouse.