FROM python:3.11-bookworm
LABEL authors="hsn8086"


WORKDIR /app

#RUN addgroup hcn-bot
#RUN adduser hcn-bot --ingroup hcn-bot
#RUN echo "root:$(echo $RANDOM$RANDOM$RANDOM$RANDOM$RANDOM | sha512sum | cut -d " " -f 1 )" | chpasswd
#RUN echo "hcn-bot:$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 20)" | chpasswd
#
#RUN chown hcn-bot:hcn-bot /app

USER root
COPY . /app
# download chrome
RUN apt update && apt install chromium chromium-driver -y -q
RUN pip install poetry

#USER hcn-bot
RUN poetry install
ENTRYPOINT ["poetry", "run", "python", "start.py"]


