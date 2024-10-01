FROM python:3.12.6-slim

WORKDIR /opt/api

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /opt/api

EXPOSE 7000

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "7000"]