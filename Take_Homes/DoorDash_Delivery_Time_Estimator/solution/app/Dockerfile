FROM python:3.7
RUN mkdir -p /doordash/app
WORKDIR /doordash/

ENV PYTHONPATH "${PYTONPATH}:/doordash/"

COPY requirements.txt ./
RUN pip install -r requirements.txt

