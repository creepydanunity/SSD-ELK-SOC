#!/usr/bin/env bash
BEATS_HOST=localhost
BEATS_PORT=5044

send_to_logstash() {
  echo "$1" | nc $BEATS_HOST $BEATS_PORT
}

while true; do
  ts=$(date +"%Y-%m-%dT%H:%M:%S.%3NZ")

  # 1) rhost line
  line1="$(date +"%Y-%m-%dT%H:%M:%S.%3N") webserver rhost=10.11.12.13 some other text"
  send_to_logstash "$line1"

  # 2) backend log — match /var/log/backend_logs/ grok
  backend_ts=$(date +"%Y-%m-%d %H:%M:%S,%3N")
  echo "$backend_ts - 208.109.231.95 - app - INFO - Search query: ' OR 1=1 --" >> /var/log/backend_logs/app.log

  # 3) backend fetch products 
  echo "$backend_ts - 101.19.17.63 - app - INFO - Fetching all products" >> /var/log/backend_logs/app.log

  # 4) login success (no SQL tag)
  echo "$backend_ts - 101.13.15.13 - app - INFO - Login successful for user: alice" >> /var/log/backend_logs/app.log

  # 5) XSS payload
  echo "$backend_ts - 101.13.15.13 - app - INFO - <script>alert('xss')</script> executed on page, onclick=\"stealCookie()\"" >> /var/log/backend_logs/app.log

  # 6) big bytes to trigger buffer overflow tag
  echo "$backend_ts - 192.168.1.1 - app - INFO - payload: 20000 bytes" >> /var/log/backend_logs/app.log

  # 7) simulate a domain indicator match
  echo "$backend_ts - 101.13.15.13 - test - INFO - {\"domain\": \"cebucafe.net\", \"message\": \"dummy\"}" >> /var/log/test_logs/test.log

  # 8) simulate an email indicator match
  echo "$backend_ts - 101.13.15.13 - test - INFO - {\"email\": \"badguy@example.com\", \"message\": \"dummy\"}" >> /var/log/test_logs/test.log

  sleep 30
done
