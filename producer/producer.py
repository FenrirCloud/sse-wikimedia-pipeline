import json
import time
import sseclient
import requests
from kafka import KafkaProducer

def create_producer():
    """Creates a Kafka producer instance."""
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='localhost:29092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Kafka Producer connected successfully.")
            return producer
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def stream_wikimedia_events(producer, topic):
    """
    Connects to the Wikimedia SSE stream and sends events to a Kafka topic.
    """
    url = 'https://stream.wikimedia.org/v2/stream/recentchange'
    headers = {'Accept': 'text/event-stream'}
    
    while True:
        try:
            response = requests.get(url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes
            client = sseclient.SSEClient(response)
            
            print(f"Successfully connected to Wikimedia stream. Listening for events...")

            for event in client.events():
                if event.event == 'message' and event.data:
                    try:
                        data = json.loads(event.data)
                        producer.send(topic, value=data)
                        # Optional: Print the title of the page being edited
                        print(f"Sent edit event for page: {data.get('title', 'N/A')}")
                    except json.JSONDecodeError:
                        print(f"Failed to decode JSON: {event.data}")
                    except Exception as e:
                        print(f"An error occurred while sending data: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Connection to Wikimedia stream failed: {e}. Reconnecting in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Reconnecting in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    KAFKA_TOPIC = "wikipedia_edits_raw"
    kafka_producer = create_producer()
    stream_wikimedia_events(kafka_producer, KAFKA_TOPIC)