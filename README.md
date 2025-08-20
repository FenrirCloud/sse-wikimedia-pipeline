# SSE Wikimedia Pipeline

## Overview
This project streams Wikimedia edits via SSE, pushes them to Kafka, processes them with Spark, and stores results in MinIO.

## Setup

1. **Install dependencies**
   ```
   pip install -r producer/requirements.txt
   ```

2. **Start services**
   ```
   docker-compose up
   ```

3. **Run the producer**
   ```
   python producer/sse_producer.py
   ```

4. **Run the Spark consumer**
   ```
   docker exec -it spark-master /opt/bitnami/spark/bin/spark-submit /opt/bitnami/spark/app/spark_consumer/spark_consumer.py
   ```

## Notes
- Ensure the Kafka topic `wikipedia_edits_raw` and MinIO bucket `wikipedia` exist.
- MinIO credentials are set in `.env`.