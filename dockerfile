FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose app port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
