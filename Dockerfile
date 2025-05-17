# Use a slim OpenJDK 11 image (Java is already installed here)
FROM openjdk:11-jre-slim

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Flask
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your server code and dpt.jar
COPY protection_server.py dpt.jar ./

# Create upload and output directories
RUN mkdir uploads protected

EXPOSE 8080

# Launch the Flask server
CMD ["python3", "protection_server.py"]
