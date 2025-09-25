#!/bin/bash

SPARK_VERSION="3.5.0"
ICEBERG_VERSION="1.5.2"
DELTA_VERSION="3.2.0"
AWS_SDK_VERSION="2.17.230" 

# Diretório do Warehouse
export PROJECT_HOME=$(pwd)
export DELTA_WAREHOUSE_DIR="$PROJECT_HOME/warehouse/delta"
export ICEBERG_WAREHOUSE_DIR="$PROJECT_HOME/warehouse/iceberg"

# Garante que os diretórios do warehouse existam
mkdir -p $DELTA_WAREHOUSE_DIR
mkdir -p $ICEBERG_WAREHOUSE_DIR

echo "======================================================"
echo "Iniciando Jupyter Lab no ambiente Poetry..."
echo "Spark Version: $SPARK_VERSION"
echo "Delta Lake Version: $DELTA_VERSION"
echo "Iceberg Version: $ICEBERG_VERSION"
echo "Project Home: $PROJECT_HOME"
echo "======================================================"

export PYSPARK_SUBMIT_ARGS=" \
    --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:$ICEBERG_VERSION,io.delta:delta-spark_2.12:$DELTA_VERSION,software.amazon.awssdk:bundle:$AWS_SDK_VERSION \
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
    --conf spark.sql.catalog.local_iceberg=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.local_iceberg.type=hadoop \
    --conf spark.sql.catalog.local_iceberg.warehouse=$ICEBERG_WAREHOUSE_DIR \
    pyspark-shell"
    
#inicia
poetry run jupyter lab --notebook-dir=./notebooks