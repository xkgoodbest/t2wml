FROM ubuntu:16.04

MAINTAINER Divij "divijbha@isi.edu"
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise universe" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise main restricted universe multiverse" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise-updates main restricted universe multiverse" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise-backports main restricted universe multiverse"
RUN apt-get update && apt-get install -y build-essential python3.6 python3-pip python3.6-dev git
COPY . /application
WORKDIR /application
RUN python3.6 -m pip install --upgrade pip
RUN python3.6 -m pip install -r requirements.txt
RUN python3.6 -m spacy download en_core_web_sm
RUN python3.6 -m pip install https://github.com/usc-isi-i2/etk/archive/development.zip
ENV PATH=$PATH:/application
ENV PYTHONPATH /application

ENTRYPOINT ["python3.6"]
CMD ["application.py"]