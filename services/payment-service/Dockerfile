FROM python:3.11-slim

WORKDIR /app

# Copy shared modules first
COPY shared /app/shared

# Install dependencies
COPY services/payment-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/payment-service/app /app/app

EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]

