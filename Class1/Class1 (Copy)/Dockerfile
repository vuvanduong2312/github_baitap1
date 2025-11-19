# ---------- Build Stage ----------
FROM python:3.10-slim AS builder

WORKDIR /app

# Cài compiler cần thiết để build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài package vào /root/.local
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Final Stage ----------
FROM python:3.10-slim

WORKDIR /app

# Copy Python packages từ builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy toàn bộ source code
COPY . .

# Tạo user không quyền root để bảo mật
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000

# Dùng gunicorn để chạy Flask production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
