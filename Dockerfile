FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# (optional) make common folders
RUN mkdir -p static/uploads log instance database

EXPOSE 5000

# Start your Flask/OpenAPI app
CMD ["python", "app.py"]