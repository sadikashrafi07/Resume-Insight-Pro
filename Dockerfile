# Stage 1: Build Stage
FROM python:3.10-slim as builder

# Set the working directory
WORKDIR /app

# Install system dependencies for PDF processing and build essentials
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production Stage
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for PDF processing (only poppler-utils needed here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Ensure that Python uses the installed packages from /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy the app code into the container
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the app using Streamlit
CMD ["streamlit", "run", "app.py"]
