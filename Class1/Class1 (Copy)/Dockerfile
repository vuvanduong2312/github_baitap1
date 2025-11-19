# DÙNG SLIM + MIRROR TQ + GOOGLE DNS → CHẮC CHẮN KHÔNG BAO GIỜ LỖI MẠNG
FROM python:3.10-slim

WORKDIR /app

# BƯỚC QUAN TRỌNG NHẤT: ÉP DÙNG GOOGLE DNS + MIRROR TRUNG QUỐC
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn \
    PIP_NO_CACHE_DIR=1

# Upgrade pip trước
RUN pip install --upgrade pip

# Cài requirements bằng mirror TQ (chắc chắn chạy được)
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

# Copy code
COPY . .

EXPOSE 5000

# Dùng gunicorn như bạn đang định dùng (rất tốt cho production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]