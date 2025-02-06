FROM python:3.12-slim
WORKDIR /XML_WS
ADD . .
RUN pip install --upgrade pip \
 && apt update \
 && apt install -y mc nano

RUN pip install -r /XML_WS/requirements.txt
