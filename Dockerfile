FROM alpine:latest

LABEL maintainer="arnarfkr@gmail.com"

WORKDIR /app

# Prevents Python from writing pyc files and
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/venv/bin:$PATH"

# Installing Python
RUN apk update && apk add --no-cache python3=3.11.9-r0 \
&& apk add --no-cache py3-pip && python3 -m venv /venv && \
# Installing dependencies for Postgres
apk add --no-cache libpq-dev && \
apk add --no-cache gcc && \
apk add --no-cache python3-dev && \
apk add --no-cache postgresql-dev && \
apk add --no-cache musl-dev && \
apk add --no-cache tzdata

# Copy the source code into the container.
COPY . .

RUN pip install --requirement ./requirements-ci.txt

EXPOSE 80

# Create a non-privileged user that the app will run under.

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser

ENTRYPOINT ["/app/docker-runserver.sh"]
