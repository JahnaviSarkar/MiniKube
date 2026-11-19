# Use official lightweight Python image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy dependency definition and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose Flask application port
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]
