# Use the official Python 3.10 image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application will run on
EXPOSE 8080

# Start the application
CMD python app.py

