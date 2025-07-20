# Use an official lightweight Python base image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the necessary files
COPY backend/ .  # Assuming extractor.py is in backend/

# Install dependencies
RUN pip install --no-cache-dir PyMuPDF

# Create input/output directories (in case they don't exist)
RUN mkdir -p /app/input /app/output

# Default command to run the extractor
CMD ["python", "extractor.py"]
