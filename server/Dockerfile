FROM python:3.10 as python
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM alpine:3.16 as alpine
COPY --from=python /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages

RUN apk add python3
COPY app.py /app/app.py
COPY ./db /app/db
COPY ./static/templates /app/static/templates

VOLUME /app/db

WORKDIR /app
CMD python3 app.py
