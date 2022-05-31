FROM alpine:latest

LABEL maintainer="guicalare"

RUN apk add --no-cache python3 py3-pip py3-numpy
RUN apk add git

RUN git clone https://github.com/guicalare/ouraddress.git

ENV APP_PORT = "8000"
