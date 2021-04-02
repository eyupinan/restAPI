FROM python:3.7.0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY main.py /usr/src/app/
COPY db_connection.py /usr/src/app/
COPY requests.log /usr/src/app/
COPY DelayMiddleware.py /usr/src/app/
COPY producer.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY routes /usr/src/app/routes
RUN pip install -r requirements.txt
ENV TZ Europe/Istanbul
EXPOSE 5000
CMD ["python", "main.py"]

