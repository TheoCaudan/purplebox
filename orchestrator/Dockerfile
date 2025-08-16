FROM python:3.11-slim

WORKDIR /orchestrator
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /orchestrator/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY orchestrate.py /orchestrator/orchestrate.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "orchestrate.py"]
