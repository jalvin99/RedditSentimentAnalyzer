from pyspark.sql import SparkSession

def main():
    # Create or retrieve a Spark session
    spark = SparkSession.builder \
        .appName("SimpleApp") \
        .getOrCreate()

    # Create a simple DataFrame
    data = [("Alice", 34), ("Bob", 45), ("Catherine", 29)]
    columns = ["Name", "Age"]

    df = spark.createDataFrame(data, columns)

    # Show the DataFrame
    df.show()

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
