FROM amazonlinux:2

# Cài curl để dùng nếu cần
RUN yum install -y curl

# Sao chép file repo đã tạo sẵn
COPY mongodb-org.repo /etc/yum.repos.d/mongodb-org.repo

# Cài MongoDB
RUN yum install -y mongodb-org && \
    mkdir -p /data/db

# Chạy mongod foreground
CMD ["mongod", "--bind_ip", "0.0.0.0"]
