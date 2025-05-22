FROM amazonlinux:latest

RUN yum update -y && \
    yum install -y python3 python3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "run.py"]
