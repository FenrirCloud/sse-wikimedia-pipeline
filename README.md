# SSE Wikimedia Pipeline

## Overview
This project streams Wikimedia edits via SSE, pushes them to Kafka, processes them with Spark, and stores results in MinIO.

## Prerequisites

1. **Environment Variables**: Create a `.env` file in the root of the project with the following content:
   ```
   MINIO_ROOT_USER=minioadmin
   MINIO_ROOT_PASSWORD=minioadmin
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r producer/requirements.txt
   ```

3. **Create Kafka Topic and MinIO Bucket**: Run the setup script to create the necessary resources.
   ```bash
   bash setup.sh
   ```

## Running the Pipeline

1. **Start Services**:
   ```bash
   docker-compose up -d
   ```

2. **Run the Producer**: Open a new terminal and run the following command to start streaming data from Wikimedia to Kafka.
   ```bash
   python producer/producer.py
   ```

3. **Run the Spark Consumer**:
   ```bash
   docker exec -it spark-master /opt/bitnami/spark/bin/spark-submit \
     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
     /opt/bitnami/spark/app/spark_consumer/spark_consumer.py
   ```

## Notes
- The processed data will be stored in the `wikipedia` bucket in MinIO.
- You can access the MinIO console at `http://localhost:9001`.
- You can monitor the Spark jobs at `http://localhost:8080`.