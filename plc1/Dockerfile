FROM python:3.11-slim

WORKDIR /app

COPY plc_server.py .

RUN pip install pymodbus

EXPOSE 5020

CMD ["python", "plc_server.py"]