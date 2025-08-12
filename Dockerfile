FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p temp outputs logs

# Set llama server defaults (can override at runtime)
ENV LLAMA_SERVER_BASE_URL=http://127.0.0.1:8080
ENV LLAMA_MODEL=unsloth.Q4_K_M.gguf

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
