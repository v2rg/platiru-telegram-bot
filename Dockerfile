FROM ubuntu:latest
LABEL authors="v2rg"

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install -r requirements.txt

COPY . /platiru_telegram_bot

ENTRYPOINT ["python", "/platiru_telegram_bot/main.py"]
