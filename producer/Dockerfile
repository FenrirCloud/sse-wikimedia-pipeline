# Dockerfile for the producer service

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the producer application's code into the container at /app
COPY . .

# The command to run when the container starts (we will override this for one-off scripts)
# For now, we can just make it wait, or you can specify your main script here.
CMD ["python", "producer.py"]