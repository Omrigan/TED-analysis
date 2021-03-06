FROM ubuntu:14.04
MAINTAINER Oleg Vasilev <omrigann@gmail.com>
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y tar \
                   git \
                   curl \
                   nano \
                   wget \
                   dialog \
                   net-tools \
                   build-essential
RUN apt-get install -y python3 python3-dev python3-pip python python-pip python-dev
RUN pip3 install --upgrade pip
ADD . /root/ted_talks
RUN pip3 install --upgrade  -r /root/ted_talks/requirements.txt
WORKDIR /root/ted_talks
CMD python3 /root/ted_talks/main.py