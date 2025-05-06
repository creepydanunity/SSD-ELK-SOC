FROM python:3.9-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      gcc libpq-dev \
      rsyslog \
      netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY rsyslog.conf /etc/rsyslog.conf

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN mkdir -p /var/log/test_logs
RUN touch /var/log/test_logs/test.log

RUN pip install supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-n"]
