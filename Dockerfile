FROM python:3.8-slim-buster

# install tesseract dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y libtesseract-dev && \
    apt-get install -y tesseract-ocr-[ukr] && \
    apt-get install -y tesseract-ocr-[rus] && \
    apt-get install -y ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# set work dir
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app/