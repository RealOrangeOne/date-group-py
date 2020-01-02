FROM python:3.8.1-alpine3.11

COPY date-group.py /bin/date-group
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["date-group"]
