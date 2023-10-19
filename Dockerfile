FROM python:3.10.12
USER root

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt /root/

RUN apt-get install -y sqlite3 vim less \
  && pip install --upgrade pip \
  && pip install --upgrade setuptools
RUN apt-get install -y libatlas-base-dev

RUN pip install -r /root/requirements.txt
