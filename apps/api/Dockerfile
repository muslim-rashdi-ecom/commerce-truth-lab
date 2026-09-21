FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY apps/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY packages/ /app/packages/
COPY apps/api/ /app/api/
COPY data/ /app/data/

WORKDIR /app/api

ENV PYTHONPATH=/app/packages

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
