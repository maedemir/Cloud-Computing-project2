FROM python:3.11.0a6-alpine3.15
WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python Price-Server.py   
# 5000 is the port number