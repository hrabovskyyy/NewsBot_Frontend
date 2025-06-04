FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH=/app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Kyiv /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

CMD ["python", "-m", "bot"]