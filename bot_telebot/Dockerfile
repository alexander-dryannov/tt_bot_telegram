FROM python:latest

WORKDIR /src/app/src/telebot

COPY bot.py .

COPY requirements.txt .

COPY .env .

RUN  /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "./bot.py"]