FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt /app/

# Add dependencies for installing uwsgi
RUN apt-get update -y && apt-get install -y gcc python3-dev musl-dev
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts directory first
COPY scripts/ /app/scripts/
# Make scripts executable
RUN chmod +x /app/scripts/django-init.sh
RUN chmod +x /app/scripts/wait-for-it.sh

# Add /scripts to the PATH environment variable
ENV PATH="/app/scripts:${PATH}"

# Copy the rest of the application
COPY . /app/