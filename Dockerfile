# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install uv

# Install dependencies
RUN uv pip install --system --no-cache

# Copy project files
COPY . .

# Default command
CMD ["python", "main.py"]
