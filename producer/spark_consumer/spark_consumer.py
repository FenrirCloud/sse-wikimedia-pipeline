import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, BooleanType, DoubleType
from pyspark.sql.functions import from_json, col

# Load environment variables from .env file
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")

# S3-compatible (MinIO) settings
MINIO_ENDPOINT = "http://minio:9000"
S3_BUCKET_NAME = "wikipedia"

def main():
    """
    Main function to run the Spark Structured Streaming job.
    """
    spark = (
        SparkSession.builder.appName("WikipediaStreamProcessor")
        .master("spark://spark-master:7077")
        # Configure S3A filesystem for MinIO
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("WARN")
    print("Spark Session created successfully.")

    # Define the schema for the incoming JSON data
    schema = StructType([
        StructField("$schema", StringType(), True),
        StructField("meta", StructType([
            StructField("uri", StringType(), True),
            StructField("request_id", StringType(), True),
            StructField("id", StringType(), True),
            StructField("dt", StringType(), True),
            StructField("domain", StringType(), True),
            StructField("stream", StringType(), True),
            StructField("topic", StringType(), True),
            StructField("partition", IntegerType(), True),
            StructField("offset", LongType(), True)
        ]), True),
        StructField("id", LongType(), True),
        StructField("type", StringType(), True),
        StructField("namespace", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("comment", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("user", StringType(), True),
        StructField("bot", BooleanType(), True),
        StructField("minor", BooleanType(), True),
        StructField("patrolled", BooleanType(), True),
        StructField("length", StructType([
            StructField("old", IntegerType(), True),
            StructField("new", IntegerType(), True)
        ]), True),
        StructField("revision", StructType([
            StructField("old", IntegerType(), True),
            StructField("new", IntegerType(), True)
        ]), True),
        StructField("server_url", StringType(), True),
        StructField("server_name", StringType(), True),
        StructField("server_script_path", StringType(), True),
        StructField("wiki", StringType(), True),
        StructField("parsedcomment", StringType(), True),
    ])

    # Read from Kafka
    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "wikipedia_edits_raw")
        .option("startingOffsets", "earliest")
        .load()
    )

    # Parse the JSON from the 'value' column
    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # Flatten the DataFrame
    flattened_df = parsed_df.select(
        col("id").alias("edit_id"),
        col("type"),
        col("title"),
        col("user"),
        col("bot"),
        col("minor"),
        col("comment"),
        col("wiki"),
        col("server_name"),
        col("timestamp"),
        col("meta.domain").alias("domain"),
        col("meta.uri").alias("uri"),
        col("length.old").alias("old_length"),
        col("length.new").alias("new_length"),
        col("revision.old").alias("old_revision"),
        col("revision.new").alias("new_revision"),
    )

    # Write the flattened data to S3 in Parquet format
    query = (
        flattened_df.writeStream.format("parquet")
        .option("path", f"s3a://{S3_BUCKET_NAME}/edits")
        .option("checkpointLocation", f"s3a://{S3_BUCKET_NAME}/checkpoints/wikipedia_edits")
        .trigger(processingTime="2 minutes")
        .start()
    )

    print("Streaming query started. Writing to MinIO...")
    query.awaitTermination()

if __name__ == "__main__":
    main()