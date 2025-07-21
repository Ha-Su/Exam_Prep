# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port 8502 (custom Streamlit port)
EXPOSE 8502

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health

# Run the Streamlit app
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8502", "--server.address=0.0.0.0"] 