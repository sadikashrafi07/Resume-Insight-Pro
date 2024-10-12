# Use Python 3.10 (or Python 3.11 if needed)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies for PDF processing (Poppler)
RUN apt-get update && apt-get install -y poppler-utils

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the app using Streamlit
CMD ["streamlit", "run", "app.py"]
