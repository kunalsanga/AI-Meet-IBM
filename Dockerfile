# Use official Python 3.10 image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"] 