FROM python:3.7.0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY main.py /usr/src/app/
COPY connections_config.py /usr/src/app/
COPY requests.log /usr/src/app/
COPY DelayMiddleware.py /usr/src/app/
COPY producer.py /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=localhost
EXPOSE 5000
CMD ["python", "main.py"]

