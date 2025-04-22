FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y gcc build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY . .

RUN /root/.cargo/bin/uv pip install --upgrade pip && \
    /root/.cargo/bin/uv pip install -e .[cli]

CMD ["/root/.cargo/bin/uv", "run", "--with", "mcp[cli]", "mcp", "run", "k8s_pilot.py"]
