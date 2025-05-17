FROM python:3.10-slim

# Fix apt and install java
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY protection_server.py .
COPY dpt.jar .

RUN mkdir uploads

EXPOSE 8080

CMD ["python", "protection_server.py"]
