FROM python:3.12-slim
# Copy the necessary files as the root user
COPY requirements.txt requirements.txt
COPY api api
COPY crawler crawler

# Install Python packages system-wide
RUN pip3 install --no-cache-dir -r requirements.txt


# Expose the port and start the application
CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
