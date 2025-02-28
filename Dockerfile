FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Add /scripts to the PATH environment variable
ENV PATH="/scripts:${PATH}"

# Set the working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Add dependencies for installing uwsgi
RUN apt-get update -y && apt-get install -y gcc python3-dev musl-dev
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x scripts/django-init.sh
RUN chmod +x scripts/wait-for-it.sh

# Copy the current directory contents into the container at /app
COPY . .
COPY ./scripts /scripts

# Make the scripts accessible by all users
RUN chmod +x /scripts/*
RUN chmod +x /scripts/wait-for-it.sh
RUN chmod +x /scripts/django-init.sh


#CMD ["./scripts/entrypoint.sh"]