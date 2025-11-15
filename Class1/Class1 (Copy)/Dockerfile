
# Sử dụng image Python chính thức
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Expose port Flask
EXPOSE 5000

# Lệnh khởi chạy ứng dụng
CMD ["python", "run.py"]
