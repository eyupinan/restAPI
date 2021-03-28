FROM python:3.7.0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY dashboard.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY assets /usr/src/app/assets
RUN pip install -r requirements.txt
EXPOSE 8050
CMD ["python", "dashboard.py"]

