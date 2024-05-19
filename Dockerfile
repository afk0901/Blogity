FROM alpine:latest

LABEL maintainer="arnarfkr@gmail.com"

WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Installing Python
RUN apk update && apk add --no-cache python3=3.11.9-r0 \
&& apk add --no-cache py3-pip && python3 -m venv /venv && \
# Installing dependencies for Postgres
apk add --no-cache libpq-dev && \
apk add --no-cache gcc && \
apk add --no-cache python3-dev && \
apk add --no-cache postgresql-dev && \
apk add --no-cache musl-dev 

ENV PATH="/venv/bin:$PATH"

# Temporarly accessing requirments.txt and install project dependencies
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt

# Copy the source code into the container.
COPY . .

EXPOSE 80

# Create a non-privileged user that the app will run under.

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser

ENTRYPOINT ["/app/docker-runserver.sh"]
