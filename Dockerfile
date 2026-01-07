FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

CMD ["python", "main.py"]
