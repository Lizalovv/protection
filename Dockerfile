FROM python:3.10-slim

# Install OpenJDK 11 for Java support
RUN apt-get update && apt-get install -y openjdk-11-jre-headless

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy server code aur dpt.jar (tujhe dpt.jar apne repo mein dalna hoga)
COPY protection_server.py .
COPY dpt.jar .

RUN mkdir uploads

EXPOSE 8080

CMD ["python", "protect_server.py"]
