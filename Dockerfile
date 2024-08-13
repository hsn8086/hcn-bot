FROM python:3.11.9-alpine3.20
LABEL Author "hsn8086 <hsn8086@github.com>"


ENV PYTHONUNBUFFERED=1

ENV HOME=/tmp
RUN addgroup -S hcn-bot && adduser -S hcn-bot -G hcn-bot -h /tmp -s /bin/sh

WORKDIR /code/

# Install packages
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.sjtug.sjtu.edu.cn/g' /etc/apk/repositories
RUN apk update && \
    apk add libxslt-dev libxml2-dev gcc g++ libffi-dev musl-dev linux-headers git && \
    rm  -rf /tmp/* /var/cache/apk/*

RUN echo "root:$(echo $RANDOM$RANDOM$RANDOM$RANDOM$RANDOM | sha512sum | cut -d " " -f 1 )" | chpasswd
RUN echo "hcn-bot:$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 20)" | chpasswd

RUN chown hcn-bot:hcn-bot /code

USER hcn-bot

COPY ./hcn-bot-building /code

USER root

RUN pip install poetry

USER hcn-bot

RUN poetry install

USER root

RUN apk del libffi-dev musl-dev linux-headers git

USER hcn-bot

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
