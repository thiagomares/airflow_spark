import os
from pyspark.sql import SparkSession

def main():
    # Inicializar a sessão do Spark
    spark = SparkSession.builder \
        .appName("ExportarParaParquet") \
        .getOrCreate()

    # Exemplo simples: criar um DataFrame e exibir
    data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
    columns = ["Name", "Value"]
    df = spark.createDataFrame(data, columns)

    df.show()

    # Escrever os dados em Parquet
    df.write \
        .mode("overwrite") \
        .parquet("./include/dados.parquet")

    # Parar a sessão do Spark
    spark.stop()

if __name__ == "__main__":
    main()
