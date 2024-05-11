# Use an official base image
FROM --platform=linux/arm64/v8 ubuntu:latest

WORKDIR /app

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone your Git repository
RUN git clone --branch dev https://github.com/ganand2021/blockpenn-python.git

WORKDIR /app/blockpenn-python

RUN chmod +x pkg_install_docker.sh

RUN ./pkg_install_docker.sh

CMD ["bash", "-c", "source /app/bpenv/bin/activate && python iot_sensor_publish_v2.py"]