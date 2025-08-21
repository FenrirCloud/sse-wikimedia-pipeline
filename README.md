<p align="center">
  <a href="" rel="noopener">
 <!-- You can replace this with a more relevant project logo if you have one -->
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">SSE Wikimedia Pipeline</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/FenrirCloud/sse-wikimedia-pipeline.svg)](https://github.com/FenrirCloud/sse-wikimedia-pipeline/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/FenrirCloud/sse-wikimedia-pipeline.svg)](https://github.com/FenrirCloud/sse-wikimedia-pipeline/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center">
    A real-time data engineering pipeline that captures live Wikimedia edits, processes them with Kafka and Spark, and stores them in MinIO.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project demonstrates a complete, real-time data engineering pipeline. It captures live Wikimedia edits using a Server-Sent Events (SSE) stream, publishes them to a Kafka topic, processes the data in near real-time using Apache Spark, and stores the results in a MinIO S3-compatible object storage.

The entire environment is containerized using Docker and Docker Compose, allowing for easy, one-command setup and consistent operation across different machines.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following software installed on your machine:

- **Docker Desktop**: The engine for running our containerized services.
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Git**: For cloning the repository.
  - [Download Git](https://git-scm.com/downloads)

### Installation

Follow these steps to set up your development environment.

1.  **Clone the Repository**

    Open your terminal and clone the project files to your local machine.

    ```bash
    git clone https://github.com/FenrirCloud/sse-wikimedia-pipeline.git
    cd sse-wikimedia-pipeline
    ```

2.  **Create the Environment File**

    Create a file named `.env` in the root of the project directory. This file holds the credentials and configuration for our services.

    ```
    # .env file

    # MinIO Credentials (used by MinIO and Spark)
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin

    # Kafka Bootstrap Server (used by the Python producer)
    KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    ```

## 🎈 Usage <a name="usage"></a>

Once the setup is complete, you can run the entire pipeline with the following commands.

1.  **Start All Background Services**

    This command will build the Docker images and start all infrastructure services (Zookeeper, Kafka, MinIO, Spark) in the background.
    
    ```bash
    docker-compose up -d
    ```
    *Wait about 30 seconds for all services to initialize.*

2.  **Run One-Time Setup Scripts**
    
    These commands create the Kafka topic and MinIO bucket that the pipeline needs. You only need to run these once.
    
    ```bash
    # Create the Kafka Topic
    docker-compose run --rm producer python create_kafka_topic.py

    # Create the MinIO Bucket
    docker-compose run --rm producer python create_minio_bucket.py
    ```

3.  **Start the Data Producer**
    
    This command starts the Python script that streams data from Wikimedia to Kafka. **Keep this terminal open** to see the live logs.
    
    ```bash
    docker-compose up producer
    ```

4.  **Run the Spark Consumer Job**
    
    **Open a new terminal window** and run the following command to submit the Spark job. This job reads from Kafka and writes the processed data to MinIO.
    
    ```bash
    docker-compose exec spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.apache.hadoop:hadoop-aws:3.3.4 /opt/bitnami/spark/app/spark_consumer.py
    ```

5.  **Monitor the Pipeline**
    - **MinIO Console**: `http://localhost:9001` (Login with credentials from `.env`)
    - **Spark UI**: `http://localhost:8080`

6.  **Stop the Pipeline**
    
    To shut down all services, press `Ctrl + C` in the producer terminal, then run:
    
    ```bash
    docker-compose down
    ```

## ⛏️ Built Using <a name = "built_using"></a>

- [Docker](https://www.docker.com/) - Containerization
- [Python](https://www.python.org/) - Producer Logic
- [Apache Kafka](https://kafka.apache.org/) - Streaming Platform
- [Apache Spark](https://spark.apache.org/) - Data Processing Engine
- [MinIO](https://min.io/) - S3-Compatible Object Storage

## ✍️ Authors <a name = "authors"></a>

- [@FenrirCloud](https://github.com/FenrirCloud) - Initial work & development

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Acknowledgment to the [Wikimedia Foundation](https://www.wikimedia.org/) for providing the real-time public event stream.