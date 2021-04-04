FROM python:3.7.0

RUN mkdir -p /usr/src/consumer
WORKDIR /usr/src/consumer
COPY consumer.py /usr/src/consumer/
COPY requirements.txt /usr/src/consumer/
RUN pip install -r requirements.txt
CMD ["python", "consumer.py"]

