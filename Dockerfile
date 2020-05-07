FROM python:3.7

RUN mkdir /source
WORKDIR /source
USER root

COPY . /source

RUN pip3 install setuptools
RUN python setup.py install 

RUN apt-get -y update
RUN apt-get -y install vim

ENTRYPOINT ["/usr/local/bin/metric-collector"]
