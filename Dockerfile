FROM alpine:latest

LABEL maintainer="guicalare"

RUN apk add --no-cache python3 py3-pip py3-numpy
RUN apk add git

RUN git clone https://github.com/guicalare/ouraddress.git

RUN pip3 install -r ./ouraddress/requirements.txt

ENV APP_PORT 8000
