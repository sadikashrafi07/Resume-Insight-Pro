# Base image with Python
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for pdf2image (Poppler)
RUN apt-get update && apt-get install -y poppler-utils

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama for LinguaLogic (custom model)
# Depending on Ollama's installation instructions
RUN curl -o- https://ollama.com/download/install.sh | bash

# Download LinguaLogic model
RUN ollama pull LinguaLogic:latest

# Copy the rest of the application code to the container
COPY . .

# Expose the Streamlit port (8501)
EXPOSE 8501

# Environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
