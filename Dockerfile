FROM alpine:latest

LABEL maintainer="arnarfkr@gmail.com"

WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

#TODO: Assuming local environment, will remove this when connecting to Google clouds.
ENV DEBUG=True
ENV PATH_TO_DJANGO_SETTINGS='Bloggity.settings.local'
ENV DJANGO_SECRET_KEY="django-insecure-kih$vse%bf+e9%4=ii7yye+s120^r8ug!5$4@k@3hnfsk+@i%r"
ENV DB_NAME="Bloggity"
ENV DB_USER="postgres"
ENV DB_PASS="12345"
ENV DB_HOST="db"
ENV DB_PORT=5432
ENV STATIC_URL="static/"
ENV ALLOWED_HOSTS="localhost,127.0.0.1"

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
