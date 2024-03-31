FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y curl apt-transport-https

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt



