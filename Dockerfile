# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (for pdf2image and Pillow, we need poppler-utils)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama for the LinguaLogic model (assuming it is supported in this environment)
RUN curl -sSfL https://ollama.com/install | sh

# Copy the requirements.txt first for efficient caching of dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project files into the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Set environment variables (these should be passed as secrets in production)
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV WEB3FORMS_ACCESS_KEY=${WEB3FORMS_ACCESS_KEY}
ENV API_URL=${API_URL}

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true"]

