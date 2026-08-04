FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg and build tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY requirements-local.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-local.txt

COPY . .

CMD ["bash"]
