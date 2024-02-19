FROM python:3.11.1-slim

WORKDIR /opt/api

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /opt/api

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "7000"]