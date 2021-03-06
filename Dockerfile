FROM alpine:latest

LABEL maintainer="guicalare"

RUN apk add --no-cache python3 py3-pip py3-numpy
RUN apk add git

#RUN git clone https://github.com/guicalare/ouraddress.git

COPY docker-build docker-build

RUN pip3 install -r ./docker-build/requirements.txt

ENV APP_PORT 8000

WORKDIR "docker-build"
CMD [ "python3", "ui-server.py" ]
