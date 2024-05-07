FROM alpine:latest

LABEL maintainer="arnarfkr@gmail.com"

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/

#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

#TODO: Assuming local environment, will change this when connecting to Google clouds.
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

# Switch to the non-privileged user to run the application.
#USER appuser

RUN apk update

RUN apk add --no-cache python3=3.11.9-r0 py3-pip
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# For Postgres
RUN apk add --no-cache libpq-dev gcc python3-dev postgresql-dev musl-dev

# Copy the source code into the container.
COPY . .

RUN python3 -m pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
