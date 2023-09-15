FROM python:3.7-slim

ENV TZ=Asia/Tokyo
ENV LANG=en_US.UTF-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -yq --no-install-recommends \
      ca-certificates curl git unzip yq \
    && pip install --upgrade pip

RUN git clone https://github.com/KichangKim/DeepDanbooru.git

WORKDIR /DeepDanbooru

RUN pip install -r requirements.txt
RUN pip install 'tensorflow'
RUN pip install 'pyyaml'
RUN pip install .
