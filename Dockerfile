FROM python:alpine
MAINTAINER gas1121 "jtdzhx@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn"]
CMD ["run:app -c /app/gunicorn.conf"]
