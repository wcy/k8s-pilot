FROM python:3.13-slim

# set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy project files
COPY . /app

# Install pip dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Start the MCP server
CMD ["python", "k8s_pilot.py"]