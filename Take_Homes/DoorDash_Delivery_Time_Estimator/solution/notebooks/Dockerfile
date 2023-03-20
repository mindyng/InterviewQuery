FROM python:3.7
RUN mkdir -p /doordash/app
RUN mkdir -p /doordash/notebooks

ENV PYTHONPATH "${PYTONPATH}:/doordash/"

COPY notebooks/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

