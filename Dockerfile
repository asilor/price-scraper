FROM python:slim

WORKDIR /app

RUN apt update && apt -y install cron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY crontab /etc/cron.d/crontab

CMD ["cron", "-f"]