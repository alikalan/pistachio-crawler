FROM selenium/standalone-chrome:latest

# Switch to the root user to perform administrative tasks
USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install necessary dependencies
RUN apt-get install -y \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set up the environment
RUN useradd -m seleniumuser

# Switch to the new user's home directory
WORKDIR /home/seleniumuser

# Copy the necessary files as the root user
COPY requirements.txt requirements.txt
COPY params.py params.py
COPY api api
COPY crawler crawler

# Install Python packages system-wide
RUN pip3 install --no-cache-dir -r requirements.txt

# Change ownership of the home directory to the non-root user
RUN chown -R seleniumuser:seleniumuser /home/seleniumuser

# Switch to the non-root user
USER seleniumuser

# Set the environment variable to indicate the container environment
ENV RUN_ENV=docker

# Expose the port and start the application
CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
