FROM python:alpine

ENV DJANGO_SETTINGS_MODULE=delivery_app.settings


RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt --use-deprecated=legacy-resolver

RUN mkdir -p /opt/delivery_app/

WORKDIR /opt/delivery_app/
COPY . /opt/delivery_app/

EXPOSE 8000