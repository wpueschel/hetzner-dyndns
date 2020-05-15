FROM python:3-alpine

COPY requirements.txt /
COPY config.yml /
COPY hetzner-dyndns.py /

RUN pip install -r /requirements.txt

