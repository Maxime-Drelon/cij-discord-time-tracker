FROM python:3.9-slim

WORKDIR /app

RUN pip install requests schedule
COPY . .

CMD ["python", "-u", "main.py"]