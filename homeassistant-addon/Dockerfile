FROM python:3.12-alpine

# Install jq for config parsing
RUN apk add --no-cache jq

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy bot files
COPY bot.py /app/
COPY run.sh /app/

# Make run script executable
RUN chmod +x /app/run.sh

# Run the startup script
CMD ["/app/run.sh"]
