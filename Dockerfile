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
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y python3-numpy python3-scipy python3-matplotlib ipython3 ipython3-notebook \
    python3-pandas  python3-nose
ENV LANG en_US.UTF-8
ADD . /var/www/ted-talks
RUN pip3 install -r /var/www/ted-talks/requirements.txt
EXPOSE 80
CMD python3 main.py