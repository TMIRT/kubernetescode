# syntax=docker/dockerfile:1

FROM python:3.14-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appgroup && useradd -r -g appgroup -m -s /sbin/nologin flaskuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R flaskuser:appgroup /app

USER flaskuser

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
