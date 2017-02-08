FROM python:2.7

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT make html