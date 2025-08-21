from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers="kafka:9092")
topic_list = [NewTopic(name="wikipedia_edits_raw", num_partitions=1, replication_factor=1)]
try:
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print("Kafka topic 'wikipedia_edits_raw' created.")
except Exception as e:
    print(f"Topic creation error or topic already exists: {e}")