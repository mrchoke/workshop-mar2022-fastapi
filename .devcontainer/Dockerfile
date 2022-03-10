FROM python:3.10-slim

LABEL maintainer="Supphachoke Suntiwichaya <mrchoke@gmail.com>"

ENV TZ=Asia/Bangkok

RUN apt update \
  && apt install -y \
  locales \
  python3-dev \
  libpq-dev \
  python3-pip 


COPY requires.txt /requires.txt
RUN pip install --no-cache-dir   -U pip && pip install --no-cache-dir    -r /requires.txt && pip install -U uvicorn httptools

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

RUN sed --in-place '/en_US.UTF-8/s/^#//' /etc/locale.gen  \
 &&  sed --in-place '/th_TH.UTF-8/s/^#//' /etc/locale.gen \
 && locale-gen

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


COPY ./app /app

WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["/start.sh"]
