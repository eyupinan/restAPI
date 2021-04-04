FROM python:3.7.0

RUN mkdir -p /usr/src/dashboard
WORKDIR /usr/src/dashboard
COPY dashboard.py /usr/src/dashboard/
COPY requirements.txt /usr/src/dashboard/
COPY assets /usr/src/dashboard/assets
RUN pip install -r requirements.txt
EXPOSE 8050
ENV TZ Europe/Istanbul
CMD ["python", "dashboard.py"]

