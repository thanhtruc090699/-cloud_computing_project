FROM amazonlinux:2


RUN yum install -y curl


COPY mongodb-org.repo /etc/yum.repos.d/mongodb-org.repo


RUN yum install -y mongodb-org && \
    mkdir -p /data/db


CMD ["mongod", "--bind_ip", "0.0.0.0"]
