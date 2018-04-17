FROM ubuntu:16.04
MAINTAINER luiza.sarzyniec@qwant.com

ENV \
  LANG=C.UTF-8 \
  TZ=Europe/Paris \
  DISPLAY=:0 \
  TF_CPP_MIN_LOG_LEVEL=2

RUN apt-get update \
  && apt-get install -y git libhunspell-dev \
  && apt-get install -y python3 python3-pip python3-tk \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /src
WORKDIR /src

COPY setup.py requirements.txt /src/
RUN pip3 install -r requirements.txt --process-dependency-links \
  && python3 -m spacy download en_core_web_lg \
  && python3 -m spacy download en_vectors_web_lg \
  && python3 -m spacy download fr_core_news_md

CMD python3
