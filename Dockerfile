# start with a base image
# FROM ubuntu:16.04
FROM python:3.7.4

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
nginx \
supervisor \
python3-pip \

&& rm -rf /var/lib/apt/lists/*
RUN echo "America/New_York" > /etc/timezone; dpkg-reconfigure -f noninteractive tzdata
# update working directories
ADD ./app /app
ADD ./config /config
ADD requirements.txt /
# install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
# run the python server

EXPOSE 5001
YELP_BEARER_TOKEN = 'Bearer 7KMbFiLj0HZ7K3QtQqW4BoVcWiYx5cbCfrYCATsq3kafy6ui-xGYRZ72GCUib6beNgOe23VDuu5zgBG6RZwfXZa26Sl0jrm54SwcBIFOZ0tkF55qaZ-SyIjciajPWnYx'
DB_MICROSERVICE_URL = 'http://localhost:5000'
CMD python3 app/app.py






