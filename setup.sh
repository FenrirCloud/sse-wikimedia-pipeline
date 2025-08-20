#!/bin/bash

# This script sets up the necessary environment for the SSE Wikimedia Pipeline project.
# It creates the Kafka topic and the MinIO bucket.

# Create Kafka Topic
echo "Creating Kafka topic 'wikipedia_edits_raw'..."
python producer/create_kafka_topic.py

# Create MinIO Bucket
echo "Creating MinIO bucket 'wikipedia'..."
python producer/create_minio_bucket.py

echo "Setup complete."
