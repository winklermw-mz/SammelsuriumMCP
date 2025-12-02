FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY tools /app/tools
COPY utils /app/utils
COPY auth /app/auth
COPY mcp_server.py /app/mcp_server.py

EXPOSE 7999

CMD ["python", "mcp_server.py"]