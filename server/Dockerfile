# Use an official Python runtime as a parent image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for application
ENV APP=/app

# Change the workdir
WORKDIR $APP

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the command to start the application
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Specify the default command to run on container start
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
