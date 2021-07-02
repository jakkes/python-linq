FROM python:3.8-slim
WORKDIR /usr/src/app

COPY linq linq
COPY tests tests
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY README.md README.md

RUN pip install -r requirements.txt
