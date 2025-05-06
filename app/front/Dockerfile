# 1) Use a minimal Alpine image
FROM alpine:3.17

# 2) Install Node.js, npm and bash (for sh -lc)
RUN apk add --no-cache \
      nodejs \
      npm \
      bash

# 3) Create a non‑root user and app directory
RUN addgroup -S appuser \
 && adduser -S -G appuser appuser \
 && mkdir -p /app \
 && chown -R appuser:appuser /app

WORKDIR /app
USER appuser

# 4) Copy package files & install deps
COPY --chown=appuser:appuser package*.json ./
RUN npm install

# 5) Copy app source
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser public/ ./public/

# 6) No inherited entrypoint, just start via shell
ENTRYPOINT []
CMD ["bash", "-lc", "npm start"]
