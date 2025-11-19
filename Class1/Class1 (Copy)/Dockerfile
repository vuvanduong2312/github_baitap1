# Sử dụng image Python chính thức
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Thêm mirror Trung Quốc để không bao giờ lỗi mạng nữa
ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ARG PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
ENV PIP_INDEX_URL=$PIP_INDEX_URL
ENV PIP_TRUSTED_HOST=$PIP_TRUSTED_HOST

# Copy requirements và cài đặt (có mirror)
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Mở port
EXPOSE 5000

# Lệnh chạy ứng dụng (thay run.py bằng tên file chính của bạn nếu khác)
CMD ["python", "run.py"]
# Nếu bạn dùng app.py + Flask CLI thì dùng dòng dưới thay thế:
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]