FROM amazonlinux:latest

RUN yum update -y && yum install -y python3 python3-pip

WORKDIR /

COPY . .



RUN pip3 install -r app/requirements.txt

ENV PYTHONPATH=/


CMD ["python3", "-m", "app.run"]
