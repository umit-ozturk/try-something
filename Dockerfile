FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y && apt-get install -y python-lz4 liblz4-tool
RUN mkdir /code
RUN mkdir /code/logs/
RUN touch /code/logs/logfile

WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD * /code/
