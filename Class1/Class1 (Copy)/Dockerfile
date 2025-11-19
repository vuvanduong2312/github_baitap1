# ---------- Base Image ----------
FROM python:3.10-bullseye

WORKDIR /app

# Copy requirements và install
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Tạo user không quyền root để bảo mật
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port
EXPOSE 5000

# Dùng gunicorn để chạy Flask production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
