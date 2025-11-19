# ---------- Build Stage ----------
FROM python:3.10-slim AS builder

WORKDIR /app

# Cài dependencies để build package (mysqlclient, cryptography,…)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Final Stage ----------
FROM python:3.10-slim

WORKDIR /app

# Runtime dependencies MySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages từ builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy toàn bộ source code
COPY . .

# Tạo user không quyền root (bảo mật)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
